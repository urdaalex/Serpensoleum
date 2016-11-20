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

def averagestuff(array):
    
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
        #print type(sen)
        n_body.append(sen.lower())
    
    whole_article = [query] + [title] + n_body
    
    toreturn = averagestuff(get_tfidfsimilarity_matrix(whole_article))
    return toreturn




def magic_fucnction(jsonfile):
    with open('saved_model.pkl', 'rb') as fid:
        model = cPickle.load(fid)
        
    X = [work_file(jsonfile)]
    irrelevant = model.predict(X)
    
    if irrelevant:
        return 0
    
    return 1