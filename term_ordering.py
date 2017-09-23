from itertools import permutations

def get_max_frequency_ordering(documents, query, term1, term2):
    """
    :rtype string
    """
    permutation_items = [query, term1, term2]
    possible_permutations = permutations(permutation_items)
    max_frequency = 0
    final_query_string = " ".join(permutation_items)
    for perm in possible_permutations:
        search_string = " ".join(perm)
        temp_frequency = 0
        for doc in documents:
            temp_frequency += doc.count(perm)
        if temp_frequency > max_frequency:
            max_frequency = temp_frequency
            final_query_string = search_string
    return final_query_string
