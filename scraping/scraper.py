import logging
from scraping.scrapers.anet_scraper import AsianetNewsScraper
from scraping.scrapers.mbhumi_scraper import MathrubhumiScraper


def scraper_main():
    # Create a list of scraper classes
    scrapers = [
        MathrubhumiScraper(),
        AsianetNewsScraper()
        # Add more scraper classes here if needed
    ]
    for scraper in scrapers:
        try:
            # Call the scraper methods for each website
            print(f"Scraping {scraper.__class__.__name__}...")
            scraper.kerala_news()
            scraper.india_news()
            scraper.world_news()
            scraper.sports_news()

            # Do something with the scraped data (e.g., save to a database or a file)
            # ...

        except Exception as e:
            logging.error(
                f"An error occurred while scraping {scraper.__class__.__name__}: {e}")
