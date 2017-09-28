""" Get best ordering of query terms for next search based on current search """

from itertools import permutations

def get_max_frequency_ordering(documents, query, term1, term2):
    """Returns ordering of terms which occurs in most queries

    :param documents: list of documents returned by Google
    :type documents: list[str]
    :param query: user query string
    :type query: str
    :param term1: first augmented term
    :type term1: str
    :param term2: second augmented term
    :type term2: str
    :return final_query_string: string with best ordering of terms
    :rtype final_query_string: string
    """
    permutation_items = [query, term1, term2]
    possible_permutations = permutations(permutation_items)
    max_frequency = 0
    final_query_string = " ".join(permutation_items)
    for perm in possible_permutations:
        search_string = " ".join(perm)
        temp_frequency = 0
        for doc in documents:
            temp_frequency += doc.count(search_string)
        if temp_frequency > max_frequency:
            max_frequency = temp_frequency
            final_query_string = search_string
    return final_query_string
