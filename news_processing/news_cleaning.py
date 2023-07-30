# For cleaning and preprocessing news data.
import logging
from nlp.nlp import nlp_main
from utils.datetime_utils import convert_to_datetime, is_datetime_within_one_hour


def news_clean_main(dict1, dict2):
    data = dict1+dict2
    input_list = nlp_main(dict1, dict2)
    # Filter the list based on datetime difference
    filtered_list = filter_by_datetime_difference(input_list)
    # Use a set comprehension to get unique tuples of (key, value) pairs
    unique_items = {tuple(item.items()) for item in filtered_list}

    # Create a new list from the unique tuples
    condition_list = [dict(item) for item in unique_items]
    filtered_data = filter_data_with_condition(data, condition_list)
    sorted_dict = sort_by_datetime(filtered_data)
    return sorted_dict


def filter_by_datetime_difference(input_list):
    result_list = []
    for entry in input_list:
        title1 = entry['title1']
        datetime1 = entry['datetime1']
        title2 = entry['title2']
        datetime2 = entry['datetime2']
        within_one_hour, title_old = is_datetime_within_one_hour(
            datetime1, datetime2)

        if within_one_hour:
            if title_old:
                result_list.append({
                    'source': 'mathrubhumi', 'clean_title': title1

                })
            else:
                result_list.append({
                    'source': 'asianetnews', 'clean_title': title2

                })
    logging.info(result_list)

    return result_list


# Print the filtered list


def filter_data_with_condition(data, condition_dict):
    """
    Filters the data list based on the condition_dict.

    Args:
        data (list): List of dictionaries containing news data.
        condition_dict (list): List of dictionaries containing conditions to match.

    Returns:
        list: Filtered data list after removing items that match the condition.
    """

    # Check if the keys exist in the item before creating the condition_set
    condition_set = set((item.get('source'), item.get('clean_title'))
                        for item in condition_dict)

    # Filter the data list to keep only items that don't match the condition
    filtered_data = [item for item in data if (
        item.get('source'), item.get('clean_title')) not in condition_set]

    return filtered_data


def sort_by_datetime(final_dict):
    # Sort the list of dictionaries based on the 'datetime' key in descending order

    sorted_dict = sorted(final_dict, key=lambda x: convert_to_datetime(
        x['datetime']), reverse=True)

    return sorted_dict
