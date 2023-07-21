from typing import List
from database.connection import get_database, get_news_collection
from database.models import NewsArticleToDb, NewsArticleFromDb

import logging


# Connect to the MongoDB database
db = get_database()
news_collection = get_news_collection()


def get_all_news() -> List[NewsArticleFromDb]:
    news_data = news_collection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]

    return news_list


def save_news_to_db(news_data: NewsArticleToDb):

    # Convert the Pydantic model to a Python dict before inserting into MongoDB(Here we add data through curl thats why)
    news_dict = news_data.model_dump()
    # Insert the news data into the "news" collection
    insert_result = news_collection.insert_one(news_dict)
    str_id = str(insert_result.inserted_id)
    news_collection.update_one({"_id": insert_result.inserted_id}, {
                               "$set": {"id": str_id}})

    logging.info("IdObject of string " + str_id + " added.")
    return "success"

    # Function to save news article data to the database


def delete_all_news():
    news_collection.delete_many({})
    return {"delete": "done"}
