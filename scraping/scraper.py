import logging
from scraping.scrapers.anet_scraper import AsianetNewsScraper
from scraping.scrapers.mbhumi_scraper import MathrubhumiScraper


def scraper_main(method_name: str):
    return_dict = []
    # Create a list of scraper classes
    scrapers = [
        MathrubhumiScraper(),
        AsianetNewsScraper()
        # Add more scraper classes here if needed
    ]

    for scrape in scrapers:
        try:

            # Call the scraper methods for each website
            print(f"Scraping {scrape.__class__.__name__}...")
            out_dict = getattr(scrape, method_name)()

            return_dict.append(out_dict)

            logging.info('1')

            # Do something with the scraped data (e.g., save to a database or a file)
            # ...

        except Exception as e:
            logging.error(
                f"An error occurred while scraping {scrape.__class__.__name__}: {e}")
    return return_dict
    logging.info(return_dict[0])
    logging.info(return_dict[1])
