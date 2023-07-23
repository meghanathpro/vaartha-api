import imghdr
from typing import List
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import logging

from utils.string_utils import extract_title_from_url


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
            # Create a dictionary with the extracted data
            news_data = {
                "datetime": datetime.text.strip(),
                "content": content.text.strip(),
                "article_link": article_link,
                "image_link": image_link
            }
            # Append the dictionary to the list
            news_data_list.append(news_data)

    logging.info(news_data_list)
    return


def test_out():

    # scrape_data_anet(anet_url, anet_kerala_url, 'kerala')
    # scrape_data_anet(anet_url, anet_world_url, 'world')
    # scrape_data_anet(anet_url, anet_india_url, 'india')
    # my_data = scrape_data_anet(anet_url, anet_sports_url, 'sports')
    my_data2 = scrape_data_anet(anet_url, anet_cricket_url, 'cricket')
    # my_data2 = scrape_data_anet(anet_url, anet_football_url, 'sports')

    # logging.info(my_data)
    logging.info(my_data2)

    return
