from typing import List
from datetime import datetime


def sort_sports_news(sports_news: List):
    # Convert "datetime" values to datetime objects
    for item in sports_news:
        item["datetime"] = datetime.strptime(
            item["datetime"], '%Y-%m-%d %H:%M')

    # Sort the list in descending order based on "num" values
    sorted_data = sorted(
        sports_news, key=lambda x: x["datetime"], reverse=True)

    # Convert "num" values back to string format
    for item in sorted_data:
        item["datetime"] = item["datetime"].strftime('%Y-%m-%d %H:%M')

    return sorted_data
