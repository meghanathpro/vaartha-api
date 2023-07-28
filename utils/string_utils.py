import re


def extract_title_from_url(url):
    # Define a regex pattern to match the title part of the URL
    pattern = r'/([^/]+)-\d+\.\d+$'

    # Use re.search to find the match in the URL
    match = re.search(pattern, url)

    if match:
        # Extract the matched title and replace hyphens with spaces
        return match.group(1).replace('-', ' ')

    # If no match is found, return None
    return 'None'


def extract_title_from_aneturl(url):
    # Define the regular expression pattern to match the title
    pattern = r'.*/([^/]+)-[a-z0-9]+$'

    # Use re.search to find the match
    match = re.search(pattern, url)

    # If a match is found, extract and return the title
    if match:
        return match.group(1).replace('-', ' ')
    # If no match is found, return None or raise an error, depending on your requirement
    return 'None'
