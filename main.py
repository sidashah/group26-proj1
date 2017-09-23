import numpy as np
from get_json_from_url import get_json_from_url
from build_matrix import build_term_doc_matrix
from term_ordering import get_max_frequency_ordering
import sys

np.set_printoptions(precision=3, linewidth=150)
np.set_printoptions(threshold=np.nan)


if __name__ == '__main__':
    google_api_key = str(sys.argv[1])
    search_engine_id = str(sys.argv[2])
    precision_required = float(sys.argv[3])
    query = str(sys.argv[4])
    query_words = len(query.split(" "))

    if precision_required < 0 or precision_required > 1:
        print "Enter correct precision"
        sys.exit()

    augmented_query = query

    # Iterations
    # use query, engine id and API Key to make call on Google Custom Search
    num_iteration = 0
    while True:
        num_iteration += 1
        print "Query: "+ augmented_query
        parameters = { "q" : augmented_query, "cx" : search_engine_id, "key" : google_api_key}
        json_data = get_json_from_url("https://www.googleapis.com/customsearch/v1", parameters)
        search_count = json_data['queries']['request'][0]['count']
        if num_iteration == 1 and search_count != 10:
            break
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

        if precision / search_count >= precision_required:
            # done - end the program
            print "Precision reached" + str(precision / search_count)
            break
        elif precision == 0:
            print "No search results matched"
            break

        relevant_results = []
        i = 0
        for item in json_data['items']:
            if result_feedback[i]:
                relevant_results.append(item['title'] + ' ' + item['snippet'])
            i += 1

        term_doc_matrix, index_to_term, term_to_index = build_term_doc_matrix(relevant_results, query)
        query_word_set = set()
        for word in augmented_query.split(" "):
            query_word_set.add(term_to_index[word])

        max_query_table = np.empty((0, term_doc_matrix.shape[1]), float)
        for term in query.split(" "):
            max_query_row = term_doc_matrix[term_to_index[term]].reshape((1,term_doc_matrix.shape[1]))
            max_query_table = np.concatenate((max_query_table, max_query_row), axis=0)

        while len(augmented_query.split(" ")) < query_words + (2 * num_iteration):
            row_of_max = np.argmax(max_query_table) / max_query_table.shape[1]
            col_of_max = np.argmax(max_query_table) % max_query_table.shape[1]
            if col_of_max not in query_word_set:
                query_word_set.add(col_of_max)
                augmented_query += " " + index_to_term[col_of_max]
            max_query_table[row_of_max][col_of_max] = 0
        print "Aug Query: " + augmented_query

    print "Original query: " + query
