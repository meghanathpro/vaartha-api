import re


def extract_title_from_url(url):
    # Define a regex pattern to match the title part of the URL
    pattern = r'/([^/]+)-\d+\.\d+$'

    # Use re.search to find the match in the URL
    match = re.search(pattern, url)

    if match:
        # Extract the matched title and replace hyphens with spaces
        title = match.group(1).replace('-', ' ')
        return title
    else:
        # If no match is found, return None
        return None
