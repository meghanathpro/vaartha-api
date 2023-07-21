from typing import List
from fastapi import APIRouter
from database.models import NewsArticleFromDb, NewsArticleToDb
from database.repository import delete_all_news, save_news_to_db, get_all_news

router = APIRouter()


@router.get("/news", response_model=List[NewsArticleFromDb])
def get_news():
    # Call the function to get all news data
    news_list = get_all_news()
    return news_list


@router.post("/add_news/")
def create_news(news_data: NewsArticleToDb):
    # Save the news data to the MongoDB news collection using the repository
    save_news_to_db(news_data)
    # Return a response indicating successful insertion
    return {"message": "News data saved successfully"}


@router.delete("/delete")
def delete_news():
    result_status = delete_all_news()
    return result_status
