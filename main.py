import numpy as np
from get_json_from_url import get_json_from_url
from build_matrix import build_term_doc_matrix

np.set_printoptions(precision=3, linewidth=150)
np.set_printoptions(threshold=np.nan)


if __name__ == '__main__':
    query = raw_input("Please enter your query: ")
    precision_required = float(raw_input("Precision required:"))

    # First Iteration
    # use query, engine id and API Key to make call on Google Custom Search
    json_data = get_json_from_url('http://siddharthshah.in/jaguar.txt')
    search_count = json_data['queries']['request'][0]['count']
    if search_count != 10:
        # end program over here
        pass
    result_feedback = [False] * search_count
    # display results to user and get feedback
    i = 0
    precision = 0
    for item in json_data['items']:
        print '\nTitle: ' + item['title']
        print 'Snippet: '+ item['snippet']
        user_feedback = raw_input("Is this relevant?(Y/N): ")
        while user_feedback not in ['Y', 'y', 'N', 'n']:
            user_feedback = raw_input("Please answer in terms of 'Y' or 'N': ")
        if user_feedback in ['Y', 'y']:
            result_feedback[i] = True
            precision += 1
        i += 1

    if precision / search_count > precision_required:
        # done - end the program
        pass

    relevant_results = []
    i = 0
    for item in json_data['items']:
        if result_feedback[i]:
            relevant_results.append(item['title'] + ' ' + item['snippet'])
        i += 1

    term_doc_matrix, index_to_term, term_to_index = build_term_doc_matrix(relevant_results)
    query_word_set = set()
    max_query_row = term_doc_matrix[term_to_index[query]]
    query_word_set.add(term_to_index[query])
    while len(query_word_set) < 3:
        index_of_max = np.argmax(term_doc_matrix[term_to_index[query]])
        if index_of_max not in query_word_set:
            query_word_set.add(index_of_max)
        max_query_row[index_of_max] = 0
    for elem in query_word_set:
        print index_to_term[elem]
