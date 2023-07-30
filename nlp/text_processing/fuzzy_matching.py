from fuzzywuzzy import fuzz

# Function to calculate fuzzy similarity between two titles


def calculate_fuzzy_similarity(title1, title2):
    # Calculate the token set ratio similarity using fuzzywuzzy
    # This function calculates the similarity of two strings based on their token sets
    # It accounts for partial matches, reordering, and allows some flexibility in word order
    return fuzz.token_set_ratio(title1, title2)

# Function to compare fuzzy similar titles


def compare_fuzzy_similar_titles(similar_titles, threshold=55):
    # List to store the results of fuzzy similar titles
    result = []
    # Loop through the entries in similar_titles
    for entry in similar_titles:
        # Extract titles and datetimes from the entry
        title1 = entry['title1']
        title2 = entry['title2']
        datetime1 = entry['datetime1']
        datetime2 = entry['datetime2']
        # Calculate fuzzy similarity between the titles using fuzzywuzzy
        similarity = calculate_fuzzy_similarity(title1, title2)
        # If similarity is greater than the threshold, consider them fuzzy similar
        if similarity > threshold:
            # Append the fuzzy similar titles to the result list
            result.append({
                'title1': title1,
                'datetime1': datetime1,
                'title2': title2,
                'datetime2': datetime2,

            })
    # Return the list of fuzzy similar titles
    return result
