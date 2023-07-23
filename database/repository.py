from typing import List
from database.connection import get_news_collection, get_india_news_collection, get_kerala_news_collection, get_sports_news_collection, get_world_news_collection
from database.models import NewsArticleToDb, NewsArticleFromDb

import logging


# Connect to the MongoDB database

news_collection = get_news_collection()
kerala_news_colection = get_kerala_news_collection()
india_news_colection = get_india_news_collection()
world_news_colection = get_world_news_collection()
sports_news_colection = get_sports_news_collection()


def get_all_news() -> List[NewsArticleFromDb]:
    news_data = news_collection.find()
    news_list = [NewsArticleFromDb(**news) for news in news_data]

    return news_list


def save_news_to_db(news_data: NewsArticleToDb):

    # Convert the Pydantic model to a Python dict before inserting into MongoDB(Here we add data through curl thats why)
    news_dict = news_data.model_dump()
    # Insert the news data into the "news" collection
    insert_result = news_collection.insert_one(news_dict)
    # Convert _id to string and insert that string id
    str_id = str(insert_result.inserted_id)
    news_collection.update_one({"_id": insert_result.inserted_id}, {
                               "$set": {"id": str_id}})

    logging.info("IdObject of string " + str_id + " added.")
    return "success"


def delete_all_news():
    news_collection.delete_many({})
    return {"delete": "done"}
