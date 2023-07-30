# TODO: Provide input comparing dictionaries
from nlp.text_processing.fuzzy_matching import compare_fuzzy_similar_titles
from nlp.text_processing.spacy_matching import find_similar_titles


def nlp_main(dict1, dict2):
    # Find similar titles and store the results in the 'similar_titles' list
    similar_titles = find_similar_titles(dict1, dict2)

    # Call the function to find fuzzy similar titles and store the results in 'fuzzy_similar_titles'
    fuzzy_similar_titles = compare_fuzzy_similar_titles(similar_titles)
    # Return the fuzzy similar titles

    return fuzzy_similar_titles
