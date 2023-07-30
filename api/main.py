from news_processing.news_storage import final_out
from scraping.scraper import scraper_main
from scraping.scrapers.mbhumi_scraper import test_mbhumi
from scraping.scrapers.anet_scraper import test_out
from fastapi import APIRouter
# Import the news endpoints
from api.endpoints.news import router as news_router
import logging


app = APIRouter()
app.include_router(news_router)

# Include the news router


@app.get("/")
def read_root():
    # Log an info message
    # Log an info message
    logging.info("This is an Home info message.")

    return {"Hello": "World"}

# TODO Remove the below code before deployment
# Tests for the project happens here


@app.get("/tests")
def fn_tests():
    logging.info("Test begin")
    # test_out()
    # test_mbhumi()
    # scraper_main()
    final_out()
    return {"done"}
