import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def get_cosine_count_matrix(documents, vocab_fancy_file=""):
    '''
    Takes in an array of [doc1sens, doc2sens]
    returns an array with 1 if word is there 0 if it's not for each
    '''
    vectorizer = CountVectorizer(vocabulary=load_vocab(vocab_fancy_file))
    #vectorizer = TfidfVectorizer(vocabulary=load_vocab())
    X = vectorizer.fit_transform(documents)
    #print X
    occurence_matrix = X.toarray()
    
    return occurence_matrix

def load_vocab(vocab_fancy_file=""):
    lst = []

    if (vocab_fancy_file != ""):
        of = open(vocab_fancy_file, "r")
    else:
        of = open("vocab_file_fancy.txt","r")

    for line in of:
        if len(line.strip())>0:
            lst.append(line.strip())
    of.close()
    return lst
    