from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from stop_words import get_stop_words
import numpy as np
def build_term_doc_matrix(documents):
    vectorizer = CountVectorizer(stop_words=get_stop_words())
    X = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names()
    index_to_term = {}
    term_to_index = {}
    for count, term in enumerate(words):
        index_to_term[count] = term
        term_to_index[term] = count
    result = normalize(X).toarray()
    result_transpose = np.transpose(result)
    answer = result_transpose.dot(result)
    return answer, index_to_term, term_to_index
