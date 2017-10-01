""" Main Application File """
import sys
import numpy as np
from get_json_from_url import get_json_from_url
from build_matrix import build_term_matrix
from term_ordering import get_max_frequency_ordering

#np.set_printoptions(precision=3, linewidth=150)
#np.set_printoptions(threshold=np.nan)


if __name__ == '__main__':
    # Google Custom Search API Key provided by user
    google_api_key = str(sys.argv[1])
    # Google Search Engine Id
    search_engine_id = str(sys.argv[2])
    # Precision required from user between 0 and 1.0
    precision_required = float(sys.argv[3])
    # Words queried by user
    query = str(sys.argv[4])
    augmented_query = query
    # Length of original query
    query_words_len = len(query.split(" "))

    # Exit application if user gives invalid precision
    if precision_required < 0 or precision_required > 1:
        print "please enter precision between 0 and 1 only."
        sys.exit()

    num_iteration = 0
    # Iterations
    while True:
        print "Parameters:"
        print "Client Key =  {}".format(google_api_key)
        print "Engine Key =  {}".format(search_engine_id)
        print "Query      =  {}".format(augmented_query)
        print "Precision  =  {}".format(precision_required)

        num_iteration += 1
        # Parameters to be sent to Google Custom Search API
        parameters = {"q" : augmented_query, "cx" : search_engine_id, "key" : google_api_key}
        # JSON Data retrieved from Google Custom Search API
        json_data = get_json_from_url("https://www.googleapis.com/customsearch/v1", parameters)
        # Search Result Count of the results returned by Custom Search API
        search_result_count = json_data['queries']['request'][0]['count']

        # If results returned by the first search are less than 10, exit the application
        if num_iteration == 1 and search_result_count != 10:
            print "Less than 10 results returned in first search. Exiting"
            break

        result_feedback = [False] * search_result_count
        i = 0
        precision_count = 0
        result_number = 0
        # Display results to user and get feedback
        for item in json_data['items']:
            result_number += 1
            print "\nResult {}".format(result_number)
            print 'URL: '+ item['link']
            print 'Title: ' + item['title']
            print 'Snippet: '+ item['snippet']
            user_feedback = raw_input("\nIs this relevant? (Y/N): ")
            # Get user feedback till user presses 'Y', 'y', 'N' or 'n'
            while user_feedback not in ['Y', 'y', 'N', 'n']:
                user_feedback = raw_input("Please answer in terms of 'Y' or 'N': ")
            # If user presses 'Y' or 'y', mark the result as relevant
            # and increase the precision count
            if user_feedback in ['Y', 'y']:
                result_feedback[i] = True
                precision_count += 1
            i += 1

        # If the program reaches desired precision, print the result and exit
        if precision_count / search_result_count >= precision_required:
            # done - end the program
            print "======================="
            print "FEEDBACK SUMMARY"
            print "Query {}".format(augmented_query)
            print "Precision {}".format(float(precision_count)/search_result_count)
            print "Desired precision reached, done."
            break
        # If the program reaches a precision count of zero
        # having no relevant results, exit the application
        elif precision_count == 0:
            print "======================="
            print "FEEDBACK SUMMARY"
            print "Query {}".format(augmented_query)
            print "Precision {}".format(float(precision_count)/search_result_count)
            print "No search results matched. Quitting."
            break

        # Create a list of relevant results
        relevant_results = []
        i = 0
        for item in json_data['items']:
            if result_feedback[i]:
                relevant_results.append(item['title'].lower() + ' ' + item['snippet'].lower())
            i += 1

        # Generate term matrix, index_to_term mapping and term_to_index mapping
        term_matrix, index_to_term, term_to_index = build_term_matrix(relevant_results, query)

        # Create a set of words in query to eliminate duplicacy while augmenting new word
        query_word_set = set()
        new_words = []
        for word in augmented_query.split(" "):
            query_word_set.add(term_to_index[word])

        # Getting rows from the term matrix for the words in the original query
        max_query_table = np.empty((0, term_matrix.shape[1]), float)
        for term in query.split(" "):
            max_query_row = term_matrix[term_to_index[term]].reshape((1, term_matrix.shape[1]))
            max_query_table = np.concatenate((max_query_table, max_query_row), axis=0)

        # Getting 2 new words from the relevant docs having highest
        # relevance with the terms in the query
        while len(augmented_query.split(" ")) + len(new_words) < query_words_len + (2 * num_iteration):
            # argmax returns indice of maximum value inside numpy array
            # shape[1] is the number of columns in the numpy array
            # getting row and column of the word having max relevance with the query words
            row_of_max = np.argmax(max_query_table) / max_query_table.shape[1]
            col_of_max = np.argmax(max_query_table) % max_query_table.shape[1]
            # checking if the word is already in the augmented query words 
            if col_of_max not in query_word_set:
                query_word_set.add(col_of_max)
                new_words.append(index_to_term[col_of_max])
            max_query_table[row_of_max][col_of_max] = 0

        # Printing Feedback Summary
        print "======================="
        print "FEEDBACK SUMMARY"
        print "Query {}".format(augmented_query)
        print "Precision {}".format(float(precision_count)/search_result_count)
        print "Still below the desired precision of {}".format(precision_required)
        print "Augmenting by {} {}".format(new_words[0], new_words[1])

        # Get reordered query where we arrange new words around the original results
        augmented_query = get_max_frequency_ordering(relevant_results, augmented_query, new_words[0], new_words[1])