from scraping.scraper import scraper_main


def fetch_kerala_news():
    kerala_news = scraper_main("kerala_news")
    # Return from two sources
    return kerala_news[0], kerala_news[1]
