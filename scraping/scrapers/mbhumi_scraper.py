from typing import List
from bs4 import BeautifulSoup
import re
import datetime
import requests
import logging
from utils.sorting_util import sort_sports_news
from utils.string_utils import extract_title_from_url


class MathrubhumiScraper:
    def __init__(self):
        self.base_url = 'https://www.mathrubhumi.com'

    def scrape_data(self, url_category: str, category: str) -> List[dict]:
        scraped_data = []

        try:
            response = requests.get(self.base_url+url_category)
            response.raise_for_status()  # Check for request errors
            html_content = response.content

            soup = BeautifulSoup(html_content, 'html.parser')
            section_card_contents = soup.select(
                'div.mpp-section-card-content.mpp-hover')
            span_tags = soup.find_all('span', class_='m-0 english')

            for section_card, span in zip(section_card_contents, span_tags):
                data = {}

                script_tag = span.find('script')
                pattern = r"show_time_difdate\('(\d+)'\)"
                matches = re.findall(pattern, str(script_tag))

                utc_match = int(matches[0]) / 1000

                utc_datetime = datetime.datetime.utcfromtimestamp(utc_match)
                india_datetime = utc_datetime + \
                    datetime.timedelta(hours=5, minutes=30)

                formatted_datetime = india_datetime.strftime('%Y-%m-%d %H:%M')

                twentyfour_before = datetime.datetime.now() - datetime.timedelta(hours=24)

                if india_datetime < twentyfour_before:
                    break

                data["datetime"] = formatted_datetime
                data["category"] = category
                data["source"] = "mathrubhumi"

                h1_tags = section_card.find_all('h1')
                for h1 in h1_tags:

                    data["content"] = h1.text

                a_tags = section_card.find_all('a', href=True)
                counter = 0
                for a in a_tags:
                    href_link = a['href']
                    counter += 1
                    if counter % 2 != 0:
                        data["article_link"] = self.base_url+href_link
                        data["clean_title"] = extract_title_from_url(
                            self.base_url+href_link)

                img_tags = section_card.find_all('img')
                for img in img_tags:
                    href_imglink = img['data-src']
                    # Remove the size of pic from string
                    clean_imglink = href_imglink.split("?")[0]
                    data["image_link"] = self.base_url + clean_imglink

                scraped_data.append(data)

            logging.info(f"Mathrubhumi {category} Scrape completed")

        except requests.exceptions.RequestException as e:
            logging.error(
                f"An error occurred while making the request to {self.base_url}: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        return scraped_data

        # The rest of the scraping logic here...

    def kerala_news(self):
        return self.scrape_data('/news/kerala', 'kerala')

    def india_news(self):
        return self.scrape_data('/news/india', 'india')

    def world_news(self):
        return self.scrape_data('/news/world', 'world')

    def sports_news(self):
        other_sports_news = self.scrape_data('/sports/news', 'sports')
        cricket_news = self.scrape_data('/sports/cricket', 'sports')
        football_news = self.scrape_data('/sports/football', 'sports')
        sports_news = other_sports_news + cricket_news + football_news

        return sort_sports_news(sports_news)


def test_mbhumi():
    """ scraper = MathrubhumiScraper()
    scraper.kerala_news()
    scraper.india_news()
    scraper.world_news()
    scraper.sports_news() """

    return


"""
mbumi_url = 'https://www.mathrubhumi.com'
mbhumi_kerala_url = '/news/kerala'
mbhumi_world_url = '/news/world'
mbhumi_india_url = '/news/india'
mbhumi_sports_url = '/sports/news'
mbhumi_cricket_url = '/sports/cricket'
mbhumi_football_url = '/sports/football'


def scrape_data_mbhumi(url: str, url_category: str, category: str) -> List:
    scraped_data = []

    try:
        response = requests.get(url+url_category)
        response.raise_for_status()  # Check for request errors
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')
        section_card_contents = soup.select(
            'div.mpp-section-card-content.mpp-hover')
        span_tags = soup.find_all('span', class_='m-0 english')

        for section_card, span in zip(section_card_contents, span_tags):
            data = {}

            script_tag = span.find('script')
            pattern = r"show_time_difdate\('(\d+)'\)"
            matches = re.findall(pattern, str(script_tag))

            utc_match = int(matches[0]) / 1000

            utc_datetime = datetime.datetime.utcfromtimestamp(utc_match)
            india_datetime = utc_datetime + \
                datetime.timedelta(hours=5, minutes=30)

            formatted_datetime = india_datetime.strftime('%Y-%m-%d %H:%M')

            twentyfour_before = datetime.datetime.now() - datetime.timedelta(hours=24)

            if india_datetime < twentyfour_before:
                break

            data["datetime"] = formatted_datetime
            data["category"] = category
            data["source"] = "mathrubhumi"

            h1_tags = section_card.find_all('h1')
            for h1 in h1_tags:

                data["content"] = h1.text

            a_tags = section_card.find_all('a', href=True)
            counter = 0
            for a in a_tags:
                href_link = a['href']
                counter += 1
                if counter % 2 != 0:
                    data["article_link"] = url+href_link
                    data["clean_title"] = extract_title_from_url(url+href_link)

            img_tags = section_card.find_all('img')
            for img in img_tags:
                href_imglink = img['data-src']
                # Remove the size of pic from string
                clean_imglink = href_imglink.split("?")[0]
                data["image_link"] = url + clean_imglink

            scraped_data.append(data)

            logging.info(f"Mathrubhumi {category} Scrape completed")

    except requests.exceptions.RequestException as e:
        logging.error(
            f"An error occurred while making the request to {url}: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return scraped_data


def mbhumi_kerala_news():
    return scrape_data_mbhumi(mbumi_url, mbhumi_kerala_url, 'kerala')


def mbhumi_india_news():
    return scrape_data_mbhumi(mbumi_url, mbhumi_india_url, 'india')


def mbhumi_world_news():
    return scrape_data_mbhumi(mbumi_url, mbhumi_world_url, 'world')


def mbhumi_sports_news():
    other_sports_news = scrape_data_mbhumi(
        mbumi_url, mbhumi_sports_url, 'sports')
    cricket_news = scrape_data_mbhumi(mbumi_url, mbhumi_cricket_url, 'sports')
    football_news = scrape_data_mbhumi(
        mbumi_url, mbhumi_football_url, 'sports')
    sports_news = other_sports_news+cricket_news+football_news

    return sort_sports_news(sports_news)


def test_mbhumi():
    # news = mbhumi_sports_news()
    # logging.info(news)
    return
"""
