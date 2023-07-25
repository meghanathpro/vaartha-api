from datetime import datetime, timedelta


def is_before_24_hours(input_datetime):
    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the datetime that is 24 hours ago from the current datetime
    twenty_four_hours_ago = current_datetime - timedelta(hours=24)

    # Check if the input datetime is before 24 hours ago
    if input_datetime < twenty_four_hours_ago:
        return True
    else:
        return False


def convert_to_datetime_anet(input_str):
    # Remove the time zone part from the input string
    input_str_without_tz = input_str.rsplit(' ', 1)[0]

    # Define the format of the input string
    input_format = '%b %d, %Y, %I:%M %p'

    # Parse the input string to a datetime object
    dt_obj = datetime.strptime(input_str_without_tz, input_format)
    result = is_before_24_hours(dt_obj)

    # Convert the datetime object to the desired output format
    output_format = '%Y-%m-%d %H:%M'
    output_str = dt_obj.strftime(output_format)

    return output_str, result
