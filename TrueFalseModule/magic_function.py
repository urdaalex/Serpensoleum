import json
import os
from measure_occurance import *
from sklearn import svm
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import accuracy_score
from preprocessor import *
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier

import cPickle

MODEL = None

def work_file(doc):
    '''
    Get the (tfidf array) for the file.

    Attributes:
        doc (Object): JSON object of file.
    '''
    documents = []
    body = doc['paragraphs']
    n_body = []
    for sen in body:
        spaced_out = spaceOutTxt(sen)
        without_stopwords = removeStopWords(spaced_out)
        #stemmed_paragraph = stemTxt(without_stopwords, st)
        n_body.append(without_stopwords.strip().lower())
        #n_body.append(sen.strip().lower())

        
    for sen in n_body:
        documents.append(sen)    
        
    total_doc = " ".join(documents)
    toreturn = get_cosine_count_matrix([total_doc], 'TrueFalseModule/vocab_file_fancy.txt')
    return toreturn


def tf_classifier(jsonfile, model_path=""):
    '''
    Returns 1 if true
    Returns 0 if false

    Attributes:
        jsonfile (JSON Object): Json File to be passed into model
        model_path (str): String of path to model
    '''
    # global MODEL
    # if MODEL is None:
    #     with open(model_path, 'rb') as fid:
    #         MODEL = cPickle.load(fid)
        
    X = work_file(jsonfile)
    
    true = MODEL.predict(X)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if true:
        return 1
    
    return 0


def pre_load_model(model_path):
    global MODEL

    with open(model_path, 'rb') as fid:
        MODEL = cPickle.load(fid)


#Trial To check it works:
'''
dirs = "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/1/vaccines AND autism/vaccines AND autism - 5 [autism.emedtv.com].json"

with open(dirs) as jd:
    doc = json.load(jd)

print magic_fucnction2(doc)
'''
