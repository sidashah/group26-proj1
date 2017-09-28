"""Builds numpy matrix with terms and documents and finally returns result of product with its transpose."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from stop_words import get_stop_words
import numpy as np

def build_term_matrix(documents, query):
    """Builds numpy matrix with terms and documents and finally returns result of product with its transpose.

    :param documents: list of documents returned by Google
    :type documents: list[str]
    :param query: user query string
    :type query: str
    :return answer: result of product of term-doc matrix with its transpose
    :rtype answer: numpy ndarray
    :return index_to_term: mapping of index to term in the matrix for easy reference
    :rtype index_to_term: dict
    :return term_to_index: mapping of index to term in the matrix for easy reference
    :rtype term_to_index: dict

    """
    vectorizer = CountVectorizer(stop_words=get_stop_words(query))
    term_doc_matrix = vectorizer.fit_transform(documents) # Learn the vocabulary dictionary and return term-document matrix.
    words = vectorizer.get_feature_names() # Array mapping from feature integer indices to feature name
    index_to_term = {}
    term_to_index = {}
    for count, term in enumerate(words):
        index_to_term[count] = term
        term_to_index[term] = count
    result = normalize(term_doc_matrix.astype(float)).toarray()
    result_transpose = np.transpose(result)
    answer = result_transpose.dot(result)
    return answer, index_to_term, term_to_index
