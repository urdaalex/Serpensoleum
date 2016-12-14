import json
import os
from measure_irrelevant import *
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import accuracy_score

from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier

import cPickle

MODEL = None

def averagestuff(array):
    print(array)
    title = array[0]
    top1 = array[1]
    top5 = np.average(array[1:6])
    all_avg = np.average(array)
    
    return [title,top1,top5,all_avg]

def work_file(doc):
    '''
    get the (tfidf array) for the file.
    '''

    query = doc['query'].lower()
    title = doc['title'].lower()
    body = doc['paragraphs']
    n_body = []
    for sen in body:
        n_body.append(sen.lower())
    
    whole_article = [query] + [title] + n_body
    
    toreturn = averagestuff(get_tfidfsimilarity_matrix(whole_article))
    return toreturn


def check_relevancy_of_document(jsonfile, model_path = ""):
    X = [work_file(jsonfile)]
    irrelevant = MODEL.predict(X)
    
    if irrelevant:
        return 0
    
    return 1


def pre_load_model(model_path):
    global MODEL

    with open(model_path, 'rb') as fid:
        MODEL = cPickle.load(fid)