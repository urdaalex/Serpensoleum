from sklearn import svm
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import accuracy_score

from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier

import cPickle

def get_X_Y(ff,option):
    X = []
    y = []
    
    ff = open(ff,'r')
    for line in ff:
        line = line.strip().split(",")
        
        if option == "all":
            X.append(map(float,line[:-1]))
        elif option == "all_top":
            X.append(map(float,line[1:-2]))
        else:
            #print line[option]
            X.append([float(line[option])])
            
        classification = line[-1]
        if classification == "n":
            y.append(1)
        else:
            y.append(0)
        
    ff.close()
    
    return X,y

def test_algo(X,y):
    X = np.array(X)
    y = np.array(y)
    result_arr = []
    skf = StratifiedKFold(n_splits=5)
    
    saved_result = 0
    
    
    for train, test in skf.split(X, y):
        
        #model = GaussianNB()
        #model = svm.LinearSVC()
        model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=0)
        model.fit(X[train], y[train])
        result = model.score(X[test],y[test])
        result_arr.append(result)
        
        if result > saved_result:
            saved_result = result
            with open('saved_model.pkl', 'wb') as fid:
                cPickle.dump(model, fid)             
        
    print result_arr
    print np.average(result_arr)
        
X,y = get_X_Y("test_train.txt", "all")
#test_algo(X,y)

#'''
with open('saved_model.pkl', 'rb') as fid:
    model = cPickle.load(fid)

print(model.score(X,y))
#'''