from __future__ import division, unicode_literals
import sys
import os
import cPickle as pickle
import simplejson
#from gensim.models import Word2Vec as w2v
#from gensim.models import Doc2Vec as d2v
#import logging
import nltk.data
from textblob import TextBlob
from math import log
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

# Split paragraphs by this token in order to easily retrieve them
# from the document
paragraph_splitter = "\n\n--\n\n"

'''
NOTE:
    The input data has to be parsed using the html parser AND processed
    by the preprocessor
'''

# Changed the way errors generated by word2vec are reported
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def isValid(input_args):
    '''
    Given the list of input arguments, this function will return a boolean
    indicating whether or not the inputs are valid
    '''
    proper_usage = "Input Error: One or more of the following is causing an issue\n" +\
                "\t 1) Too few or too many inputs \n" +\
                "\t 2) The input directory doesn't exist\n" +\
                "\t 3) The output directory already exists\n" +\
                "Correct usage: \n" +\
                "\t clustering_approach.py 'input_dir_name' 'output_dir_name'"

    if len(input_args) != 2 or os.path.exists(input_args[1]) \
                or not os.path.exists(input_args[0]):
        print proper_usage
        return False

    return True

def getSentences(JSON_files):
    '''
    Given a list of JSON files where each JSON file has a dictionary
    'paragraphs' which is a list of the paragraphs in the article
    represented by that JSON file, this function returns a list
    of all the sentences (each sentence will bea list of all the
    words/characters in it) in all the paragraphs of all the JSON files
    '''
    all_sentences = []
    for json in JSON_files:
        paragraphs = json['paragraphs']
        for paragraph in paragraphs:
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            sentence = ''.join(tokenizer.tokenize(paragraph))
            all_sentences.append([i for i in sentence.split(' ')])
    return all_sentences

def getDocuments(JSON_files):
    '''
    Given a list of JSON files, where each JSON file has a dictionary 'paragraphs'
    which is a list of the paragraphs in the article represented by that JSON file,
    this function returns a list of documents (each article is a document) &
    its label (list of document, label tuples), where a document representation
    of an article is the concatenation of the paragraphs it contains
    '''
    all_documents = []
    for json in JSON_files:
        paragraphs = json['paragraphs']
        label = json['actual-search-type']
        document = ''
        for paragraph in paragraphs[:-1]:
            document += paragraph + paragraph_splitter
        document += paragraphs[-1]
        all_documents.append((document, label))
    return all_documents

def getTf(word, document):
    '''
    Given a word and a document, this function returns the term frequency
    of the word in the documents
    '''
    return document.words.count(word) / len(document.words)

def getNumContaining(word, documents):
    '''
    Given a word and a list of all documents, this function returns the number
    of documents that contain word in them
    '''
    return sum(1 for doc in documents if word in doc.words)

def getIdf(word, documents):
    '''
    Given a word and a list of all documents, this function returns the
    inverse document frequency of word
    '''
    return log(len(documents) / (1 + getNumContaining(word, documents)))

def getTfIdf(word, document, documents):
    '''
    Given a word, a document, and a list of all documents, this function
    returns the tf-idf of the word relative to document (the product of
    the term frequency of word in document, multiplied by the inverse document
    frequency of the word over all documents)
    '''
    return getTf(word, document) * getIdf(word, documents)

def makeBlobs(all_documents):
    '''
    Given a list of all documents as returned by getDocuments, this function
    makes a list of documents where each document is a TextBlob
    '''
    return [TextBlob(all_documents[i][0]) for i in range(len(all_documents))]

def makeDocumentVectors(all_documents):
    '''
    Given all documents as returned by getDocuments, this function will
    return a list of tf-idf vectors representing each document. This function
    will pad document vectors with 0 until they all have the same length
    (the length of the max length document vector)
    '''
    # Make all the documents into TextBlobs
    documents = makeBlobs(all_documents)
    document_vectors = []

    # Keep track of the dimensionality of the highest dimensional tf-idf vector
    max_length = -1 * float('inf')

    # For each document, get the tf-idf of each word in it
    for doc in documents:
        document_vector = []
        for word in doc.words:
            tf_idf = getTfIdf(word, doc, documents)
            document_vector.append(tf_idf)
        if len(document_vector) > max_length:
            max_length = len(document_vector)
        document_vectors.append(np.array(document_vector))

    # Ensure that each tf-idf vector has the same dimensionality
    # by padding with 0's
    for i in range(len(document_vectors)):
        document_vectors[i] = np.append(document_vectors[i], [0] * (max_length - len(document_vectors[i])))

    return document_vectors

def getNumClusters(doc_vectors):
    '''
    Given a list of document vectors as returned by makeDocumentVectors,
    this function runs affinity propogation on the vectors to approximate
    the number of clusters the documents would fall into
    '''
    clf = AffinityPropagation()
    clf.fit(doc_vectors)
    return len(clf.cluster_centers_indices_)

def getNearestDocuments(target, documents):
    '''
    Given a target document in the form returned by makeDocumentVectors
    and the rest of the documents (also in the form returned by
    makeDocumentVectors), this function returns the indices of the set
    of documents that fall into the same cluster as the target document
    '''
    # Get the number of clusters from affinity
    num_clusters = getNumClusters(documents)

    # Cluster the documents using KMeans
    clf = KMeans(n_clusters=num_clusters)
    clf.fit(documents)

    # Find the cluster centre which is nearest to target
    min_distance = float('inf')
    min_idx = -1
    for i in range(len(clf.cluster_centers_)):
        current_distance = euclidean(clf.cluster_centers_[i], target)
        if current_distance < min_distance:
            min_distance = current_distance
            min_idx = i
    target_cluster_idx = min_idx

    # Make a list documents_in_each_cluster = [y_0, y_1, ..., y_n] where y_0
    # is a list of indices representing the documents in 'documents' that fall
    # into cluster 0, WLOG y_1 is for the documents that fall into cluster 1,
    # and so on...
    documents_in_each_cluster = [[] for i in range(num_clusters)]
    for doc_idx in range(len(documents)):
        # Get the current document
        doc = documents[doc_idx]

        # Find the cluster to which doc belongs
        closest_cluster_idx = -1
        min_distance = float('inf')
        for i in range(len(clf.cluster_centers_)):
            current_distance = euclidean(clf.cluster_centers_[i], doc)
            if current_distance < min_distance:
                min_distance = current_distance
                closest_cluster_idx = i

        # Add doc_idx to the list of document indices representing the
        # documents that belong to the cluster specified by closest_cluster_idx
        documents_in_each_cluster[closest_cluster_idx].append(doc_idx)

    return documents_in_each_cluster[target_cluster_idx]


def main(argv):
    '''
    Given the array of arguments to the program, the main method will ensure
    that the inputs are valid, if they are, the JSON files in the input
    directory will be loaded, and the clustering approach will be applied
    on the data in the input directory. The model will then be saved
    into a pickle file specified by the input arguments
    '''
    # Check that the input arguments are valid
    if not isValid(argv):
        sys.exit(1)

    # Load a list of the JSON files in the input dir
    JSON_files = []
    for filename in os.listdir(argv[0]):
        with open(os.path.join(argv[0], filename), 'r') as json_file:
            JSON_files.append(simplejson.load(json_file))

    # Get all the documents in the JSON files
    documents_and_labels = getDocuments(JSON_files)

    # Get all document vectors & the labels
    document_vectors = makeDocumentVectors(documents_and_labels)
    labels = [documents_and_labels[i][1] for i in range(len(documents_and_labels))]

    # Shuffle the data, include random state for reproducibility
    X, y = shuffle(document_vectors, labels, random_state=0)

    # Split the data (20% of data going into the test set)
    # include random state for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,
                                                       random_state=0)

    # Get the indices of the training examples and the testing examples
    # in document_vectors
    train_ex_idxs = [document_vectors.index(i) for i in X_train]
    test_ex_idxs = [document_vectors.index(i) for i in X_test]

    # Go over each test example and predict the label using the clustering
    # approach
    for i in range(len(X_test)):
        # Get the information for the current test example
        cur_test_doc = X_test[i]
        cur_test_doc_label = y_test[i]

        # Get the nearest documents to the current test example
        nearest_docs_idxs = getNearestDocuments(cur_test_doc, X_train)
        nearest_docs = [X_train[j] for j in nearest_docs_idxs]
        nearest_docs_labels = [y_train[j] for j in nearest_docs_idxs]

        # Reduce the dimensionality of the nearest_docs to be equal to
        # the number of sentences in the current test doc
        pca = PCA(n_components = )


if __name__ == "__main__":
    main(sys.argv[1:])
