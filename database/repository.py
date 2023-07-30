from typing import List
from database.connection import get_news_collection, get_india_news_collection, get_kerala_news_collection, get_sports_news_collection, get_world_news_collection
from database.models import NewsArticleToDb, NewsArticleFromDb, NewsArticleToCompare
import datetime
import logging
import csv


# Connect to the MongoDB database

news_collection = get_news_collection()
kerala_news_colection = get_kerala_news_collection()
india_news_colection = get_india_news_collection()
world_news_colection = get_world_news_collection()
sports_news_colection = get_sports_news_collection()


def get_all_news() -> List[NewsArticleFromDb]:
    news_data = news_collection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]
    logging.info("Database current list fetch completed")
    return news_list


def get_kerala_news() -> List[NewsArticleFromDb]:
    news_data = kerala_news_colection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]
    logging.info("Database kerala list fetch completed")
    return news_list


def get_india_news() -> List[NewsArticleFromDb]:
    news_data = india_news_colection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]
    logging.info("Database kerala list fetch completed")
    return news_list


def get_sports_news() -> List[NewsArticleFromDb]:
    news_data = sports_news_colection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]
    logging.info("Database kerala list fetch completed")
    return news_list


def retrive_current_list(collection):
    news_data_dicts = []
    current_data = collection.find()

    current_list = [NewsArticleToCompare(**news) for news in current_data]
    # Convert each NewsArticleToCompare object to a dictionary
    if (len(current_list) != 0):
        news_data_dicts = [item.dict() for item in current_list]
    return news_data_dicts


def compare_with_db(input_data, news_from_db):

    if (len(news_from_db) == 0):
        return input_data
    else:

        # Get a set of article links from dict2
        dict2_article_links = set(item['article_link']
                                  for item in news_from_db)
        # Filter dict1 based on unique article links
        dict_result = [
            item for item in input_data if item['article_link'] not in dict2_article_links]

        return dict_result


def save_news_to_db(news_data: List[NewsArticleToDb], collections):

    filtered_data = [NewsArticleToDb(**item) for item in news_data]
    # Convert each NewsArticleToDb object to a dictionary
    news_filtered_data = [item.dict() for item in filtered_data]

    current_list = retrive_current_list(collections)

    new_data = compare_with_db(news_filtered_data, current_list)
    if (len(new_data) != 0):
        # Convert the datetime strings from the input data to datetime objects
        for item in new_data:
            item['datetime_obj'] = datetime.datetime.strptime(
                item['datetime'], '%Y-%m-%d %H:%M')

        insert_result = collections.insert_many(new_data)
        # Convert _id to string and insert that string id for each document
        for inserted_id in insert_result.inserted_ids:
            str_id = str(inserted_id)
            collections.update_one(
                {"_id": inserted_id},
                {"$set": {"id": str_id}}
            )
    fetch_from_db_delete_older_add_to_csv(collections)

    return "success"


def fetch_from_db_delete_older_add_to_csv(collections):

    # Calculate the time 24 hours ago from the current time
    current_time = datetime.datetime.now()
    time_threshold = current_time - datetime.timedelta(hours=24)
    # Define the query to find documents older than 24 hours
    query = {"datetime_obj": {"$lt": time_threshold}}
    # Fetch the matching documents
    cursor = collections.find(query)
    # Save the documents to a CSV file
    csv_file_path = 'logs/csv_dumps/deleted_documents.csv'

    # Save the documents to a CSV file
    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['datetime', 'category', 'source',
                      'content', 'article_link', 'image_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty, if yes, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        for document in cursor:

            # Filter out additional fields not present in fieldnames
            filtered_document = {key: document[key] for key in fieldnames}

            # Write the document to the CSV file
            writer.writerow(filtered_document)
    collections.delete_many(query)

    return


def delete_all_news():
    news_collection.delete_many({})
    return {"delete": "done"}
