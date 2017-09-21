from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

def build_term_doc_matrix(documents):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names()
    print words
    result = normalize(X.toarray())
    print result