# For handling news data storage and database interactions.
from database.repository import save_news_to_db, kerala_news_colection, india_news_colection, world_news_colection, sports_news_colection
from news_processing.news_cleaning import news_clean_main
from scraping.scraper import scraper_main
import logging

# Fetching and returning after cleaning


def fetch_all_news():
    news_collections = [kerala_news_colection, india_news_colection,
                        world_news_colection, sports_news_colection]
    all_news = ["kerala_news", "india_news", "world_news", "sports_news"]

    for news, news_collection in zip(all_news, news_collections):
        all_news = scraper_main(news)
        final_news = news_clean_main(all_news[0], all_news[1])
        output = save_news_to_db(final_news, news_collection)
        logging.info(f"{news} scrapping..")
        print(output)
    # Return from two sources
    return "success"


def final_out():
    fetch_all_news()
    return
