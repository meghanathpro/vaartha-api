
from typing import List
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import logging
from utils.datetime_utils import convert_to_datetime_anet
from utils.sorting_util import sort_sports_news

from utils.string_utils import extract_title_from_aneturl


class AsianetNewsScraper:

    def __init__(self):
        self.base_url = 'https://www.asianetnews.com'

    def scrape_data(self, url_category: str, category: str) -> List[dict]:

        # Initialize an empty list to store the extracted data
        news_data_list = []
        scrape_url = self.base_url+url_category
        response = requests.get(scrape_url)
        response.raise_for_status()  # Check for request errors

        # Create a BeautifulSoup object with the HTML content
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the <div> elements with class "newcol"
        div_elements = soup.find_all('div', class_='newcol lozad')
        # div_elements = [sample_url]
        # Loop through each <div> element
        # logging.info(div_elements)

        for div in div_elements:

            # Extract the datetime, category, and source from the <div> element
            datetime_elements = div.find_all('div', class_='publishdate')
            # Extract the content from the <div> element
            content_elements = div.find_all('p')
            # Extract the article_link from the <div> element
            article_link_element = [a['href']
                                    for a in div.find_all('a', href=True)]
            # Extract the image_link from the <div> element
            image_link_elements = [img['data-src']
                                   for img in div.find_all('img', class_='lozad')]
            # Remove duplicate href's
            article_link_elements = list(
                OrderedDict.fromkeys(article_link_element))
            # logging.info(article_link_elements)
            # Loop through each usin zip
            for datetime, content, article_link, image_link in zip(datetime_elements, content_elements,  article_link_elements, image_link_elements):
                # Call the function and assign the two outputs
                formated_date, is_before_24_hours = convert_to_datetime_anet(
                    datetime.text.strip())

                if is_before_24_hours:
                    break
                article_link_full = self.base_url+article_link
                # Create a dictionary with the extracted data
                news_data = {
                    "datetime": formated_date,
                    "category": category,
                    "source": "asianetnews",
                    "content": content.text.strip(),
                    "article_link": article_link_full,
                    "clean_title": extract_title_from_aneturl(article_link_full),
                    "image_link": image_link
                }
                # Append the dictionary to the list
                news_data_list.append(news_data)
        logging.info(f"Asianetnews {category} Scrape completed")
        return news_data_list

    def kerala_news(self):
        return self.scrape_data('/kerala-news', 'kerala')

    def india_news(self):
        return self.scrape_data('/india-news', 'india')

    def world_news(self):
        return self.scrape_data('/international-news', 'world')

    def sports_news(self):
        other_sports_news = self.scrape_data('/other-sports', 'sports')
        cricket_news = self.scrape_data('/cricket-sports', 'sports')
        football_news = self.scrape_data('/football-sports', 'sports')
        sports_news = other_sports_news+cricket_news+football_news

        return sort_sports_news(sports_news)
        # Your existing anet_sports_news function goes here


def test_out():
    # Create an instance of the class
    """ scraper = AsianetNewsScraper()

    scraper.kerala_news()
    scraper.india_news()
    scraper.world_news()
    scraper.sports_news() """

    return


"""

anet_url = 'https://www.asianetnews.com'
anet_kerala_url = '/kerala-news'
anet_world_url = '/international-news'
anet_india_url = '/india-news'
anet_sports_url = '/other-sports'
anet_cricket_url = '/cricket-sports'
anet_football_url = '/football-sports'


def scrape_data_anet(url: str, url_category: str, category: str) -> List:
    # Initialize an empty list to store the extracted data
    news_data_list = []

    response = requests.get(url+url_category)
    response.raise_for_status()  # Check for request errors

    # Create a BeautifulSoup object with the HTML content
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the <div> elements with class "newcol"
    div_elements = soup.find_all('div', class_='newcol lozad')
    # div_elements = [sample_url]
    # Loop through each <div> element
    # logging.info(div_elements)

    for div in div_elements:

        # Extract the datetime, category, and source from the <div> element
        datetime_elements = div.find_all('div', class_='publishdate')
        # Extract the content from the <div> element
        content_elements = div.find_all('p')
        # Extract the article_link from the <div> element
        article_link_element = [a['href']
                                for a in div.find_all('a', href=True)]
        # Extract the image_link from the <div> element
        image_link_elements = [img['data-src']
                               for img in div.find_all('img', class_='lozad')]
        # Remove duplicate href's
        article_link_elements = list(
            OrderedDict.fromkeys(article_link_element))
        # logging.info(article_link_elements)
        # Loop through each usin zip
        for datetime, content, article_link, image_link in zip(datetime_elements, content_elements,  article_link_elements, image_link_elements):
            # Call the function and assign the two outputs
            formated_date, is_before_24_hours = convert_to_datetime_anet(
                datetime.text.strip())

            if is_before_24_hours:
                break
            # Create a dictionary with the extracted data
            news_data = {
                "datetime": formated_date,
                "category": category,
                "source": "asianetnews",
                "content": content.text.strip(),
                "article_link": url+article_link,
                "clean_title": extract_title_from_aneturl(url+article_link),
                "image_link": image_link
            }
            # Append the dictionary to the list
            news_data_list.append(news_data)
        logging.info(f"Asainetnews {category} Scrape completed")

    return news_data_list


def anet_kerala_news():
    return scrape_data_anet(anet_url, anet_kerala_url, 'kerala')


def anet_india_news():
    return scrape_data_anet(anet_url, anet_india_url, 'india')


def anet_world_news():
    return scrape_data_anet(anet_url, anet_world_url, 'world')


def anet_sports_news():
    other_sports_news = scrape_data_anet(anet_url, anet_sports_url, 'sports')
    cricket_news = scrape_data_anet(anet_url, anet_cricket_url, 'sports')
    football_news = scrape_data_anet(anet_url, anet_football_url, 'sports')
    sports_news = other_sports_news+cricket_news+football_news

    return sort_sports_news(sports_news)


def test_out():

    # my_data2 = anet_sports_news()
    # logging.info(my_data2)

    return

"""
