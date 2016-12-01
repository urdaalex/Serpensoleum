from __future__ import division, unicode_literals
import sys
import os
import cPickle as pickle
import simplejson
from textblob import TextBlob
from math import log
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from sklearn.decomposition import PCA
from sklearn.model_selection import ShuffleSplit
from sklearn.svm import SVC

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

def getNumSentences(documents):
    '''
    Given a list of documents, this function returns a list where
    the list[i] = the number of sentences in the document in
    documents[i]
    '''
    documents = makeBlobs(documents)
    return [len(document.sentences) for document in documents]

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

    # Get the number of sentences in the documents
    num_sentences = getNumSentences(documents_and_labels)

    # Keep track of the number of examples classified & the ones that were
    # wrongly predicted
    num_predictions = 0
    num_wrong = 0

    # Shuffle and split the data
    rs = ShuffleSplit(n_splits=1, train_size=0.8, test_size=0.2)
    for train_idx, test_idx in rs.split(document_vectors):
        # Get the training data
        X_train = [document_vectors[i] for i in train_idx]
        y_train = [labels[i] for i in train_idx]

        # Get the test data
        X_test = [document_vectors[j] for j in test_idx]
        y_test = [labels[j] for j in test_idx]

        # Get the number of sentences in each of the test examples
        num_sentences_in_test = [num_sentences[i] for i in test_idx]

        # Train a classifier for each test example
        for test_ex_idx in range(len(X_test)):
            # Get the test example and the number of sentences in it
            test_example = X_test[test_ex_idx]
            test_example_label = y_test[test_ex_idx]
            num_sen = num_sentences_in_test[test_ex_idx]

            # Use PCA to bring down the dimensionality of the training data
            # to the number of sentences in this particular test example
            # then reduce the test example
            try:
                pca = PCA(n_components = num_sen)
                pca.fit(X_train)
                X_train = pca.transform(X_train)
                test_example = pca.transform(test_example)
            except:
                pca = PCA(n_components = 11)
                pca.fit(X_train)
                X_train = pca.transform(X_train)
                test_example = pca.transform(test_example)

            # Train a classifier and predict the label
            clf = SVC(kernel='poly', degree=3)
            clf.fit(X_train, y_train)
            prediction = clf.predict(test_example)
            num_predictions += 1

            if(prediction != test_example_label):
                num_wrong += 1

    print float(num_wrong)/num_predictions

if __name__ == "__main__":
    main(sys.argv[1:])
