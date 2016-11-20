import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def get_tfidfsimilarity_matrix(documents):
    '''
    Takes in an array of [query, title, sen1, sen2, ...]
    Returns array of [num, num, num] where nums are tfidf sims between query and each of all
    assert len(input) == len(output)+1
    '''
    vectorizer = TfidfVectorizer(stop_words = "english")
    X = vectorizer.fit_transform(documents)
    #print X
    similarity_matrix = (X * X.T).A
    
    return similarity_matrix[:,0][1:]