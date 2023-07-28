import spacy


# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to calculate the similarity between two titles using spaCy


def calculate_similarity(title1, title2):
    # Process the titles with spaCy to create doc objects
    doc1 = nlp(title1)
    doc2 = nlp(title2)
    # Compute the similarity between the two doc objects
    return doc1.similarity(doc2)

# Function to find similar titles from two dictionaries


def find_similar_titles(dict1, dict2, threshold=0.80):
    # List to store similar titles
    similar_titles = []
    # Loop through the entries in dict1
    for entry1 in dict1:
        title1 = entry1['title']
        datetime1 = entry1['datetime']
        # Loop through the entries in dict2
        for entry2 in dict2:
            title2 = entry2['title']
            datetime2 = entry2['datetime']
            # Calculate the similarity between the titles using spaCy
            similarity = calculate_similarity(title1, title2)
            # If similarity is greater than the threshold, consider them similar
            if similarity > threshold:
                # Append the similar titles to the list
                similar_titles.append({
                    'title1': title1,
                    'datetime1': datetime1,
                    'title2': title2,
                    'datetime2': datetime2,
                    'similarity': similarity
                })
    return similar_titles


# TODO: Provide input comparing dictionaries
dict1 = []
dict2 = []

# Find similar titles and store the results in the 'similar_titles' list
similar_titles = find_similar_titles(dict1, dict2)
