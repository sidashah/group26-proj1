from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from stop_words import get_stop_words
import numpy as np
def build_term_doc_matrix(documents):
    vectorizer = CountVectorizer(stop_words=get_stop_words())
    X = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names()
    print list(enumerate(words))
    result = normalize(X).toarray()
    print(result)
    print('\n\n')
    result_transpose = np.transpose(result)
    answer = result_transpose.dot(result)
    print(answer)

    """for count, elem in enumerate(words):
    	print elem, result[0][count]
    	print elem, result[1][count]
    	print elem, result[2][count]
    	print elem, result[3][count]"""