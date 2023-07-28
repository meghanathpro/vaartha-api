# For cleaning and preprocessing news data.
from utils.datetime_utils import is_datetime_within_one_hour


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

    return result_list


# Your List of dictionaries
input_list = []

# Filter the list based on datetime difference
filtered_list = filter_by_datetime_difference(input_list)

# Print the filtered list


# Use a set comprehension to get unique tuples of (key, value) pairs
unique_items = {tuple(item.items()) for item in filtered_list}

# Create a new list from the unique tuples
result_list = [dict(item) for item in unique_items]

print(result_list)


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


condition_dict = []

data = []

# Call the function and print the filtered data
filtered_data = filter_data_with_condition(data, condition_dict)
print(filtered_data)
