from typing import List
from bs4 import BeautifulSoup
import re
import datetime
import requests
import logging

from utils.string_utils import extract_title_from_url


mbumi_url = 'https://www.mathrubhumi.com'
mbhumi_kerala_url = '/news/kerala'
mbhumi_world_url = '/news/world'
mbhumi_india_url = '/news/india'
mbhumi_sports_url = '/sports/news'
mbhumi_cricket_url = '/sports/cricket'
mbhumi_football_url = '/sports/football'


def scrape_data_mbhumi(url: str, url_category: str, category: str) -> List:
    scraped_data = []
    count = 1

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
            logging.info(twentyfour_before)
            logging.info(india_datetime)

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

            logging.info("success scraped data " + str(count))
            count += 1

    except requests.exceptions.RequestException as e:
        logging.error(
            f"An error occurred while making the request to {url}: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return scraped_data


def test_out_mbhumi():
    # scrape_data_mbhumi(mbumi_url, mbhumi_kerala_url, 'kerala')

    # scrape_data_mbhumi(mbumi_url, mbhumi_world_url, 'world')

    # my_data = scrape_data_mbhumi(mbumi_url, mbhumi_india_url, 'india')

    # scrape_data_mbhumi(mbumi_url, mbhumi_sports_url, 'sports')

    # scrape_data_mbhumi(mbumi_url, mbhumi_football_url, 'sports')
    """ my_data = scrape_data_mbhumi(mbumi_url, mbhumi_cricket_url, 'sports')
    logging.info(my_data) """

    return
