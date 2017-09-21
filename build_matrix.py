from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from stop_words import get_stop_words
def build_term_doc_matrix(documents):
    vectorizer = CountVectorizer(stop_words=get_stop_words())
    X = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names()
    print list(enumerate(words))
    result = normalize(X.toarray())
    print result