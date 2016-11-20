import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def load_document(path):
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def get_class_query(dir2,ff):
    #This is the not parsed file
    #It contains "actual-search-type", "query"
    #return (query, actual-search-type)
    
    doc = load_document(dir2+ff)
    #print doc.keys()
    query = doc["query"]
    query = query.lower()
    return (query,doc["actual-search-type"])

def get_sentences(dir1,ff):
    #This takes in the parsed file
    #"paragraphs is the sentences"
    #Return all the sentences lowered case
    doc = load_document(dir1+ff)
    sentences = doc["paragraphs"]
    n_sen = []
    for sen in sentences:
        n_sen.append(sen.lower())
    
    return n_sen

def get_tfidfsimilarity_matrix(documents):
    vectorizer = TfidfVectorizer(stop_words = "english")
    X = vectorizer.fit_transform(documents)
    #print X
    similarity_matrix = (X * X.T).A
    
    return similarity_matrix[:,0][1:]

def numbers(query,sentences):
    documents = [query]+sentences
    
    all_nums = get_tfidfsimilarity_matrix(documents)
    
    top_1 = max(all_nums)
    if len(all_nums) >5:
        top_5 = np.average(sorted(all_nums,reverse=True)[:5])
    else:
        top_5 = np.average(all_nums)
    avg = np.average(all_nums)
    
    return (top_1,top_5,avg)

def create_file(dir1,dir2):
    #not parsed
    #dir_1
    #parsed
    #dir_2 = ""
    
    files = os.listdir(dir2)
    toreturn = []
    
    for ff in files:
        query,classification = get_class_query(dir1,ff)
        sentences = get_sentences(dir2,ff)
        
        top_1,top_5,avg = numbers(query,sentences)
        
        if classification != "n":
            classification = "q"
        
        toreturn.append([top_1,top_5,avg,classification,ff])
        
    return toreturn

def get_whole_array():
    '''
    This function calls the work function for every folder pairing
    Each call returns an array with top_1,top_5,avg,classification
    Combine all of them together, and print to file.
    We can then use machine learning to get it (Cross validation)
    '''
    towrite = []
    
    dir1_lst = ["/home/b/Documents/00490/Alex/csc490/data/accredited/",
                "/home/b/Documents/00490/Alex/csc490/data/accredited-2/",
                "/home/b/Documents/00490/Alex/csc490/data/blogs/",
                "/home/b/Documents/00490/Alex/csc490/data/neg-search/",
                "/home/b/Documents/00490/Alex/csc490/data/neg-search-2/"]
    dir2_lst = ["/home/b/Documents/00490/Alex/csc490/data/parsed_accredited/vaccines AND autism/",
                "/home/b/Documents/00490/Alex/csc490/data/parsed_accredited-2/proof vaccines dont cause autism/" ,
                "/home/b/Documents/00490/Alex/csc490/data/parsed_blogs/vaccines AND autism/",
                "/home/b/Documents/00490/Alex/csc490/data/parsed-neg-search/vaccines cause autism supporting evidence/",
                "/home/b/Documents/00490/Alex/csc490/data/parsed_neg_search_2/proof vaccines cause autism/"]
    
    for i in range(len(dir1_lst)):
        towrite.extend(create_file(dir1_lst[i],dir2_lst[i]))
        
    wf = open("irrelevancy_arff_type.txt",'w')
    for i in towrite:
        i = i[:-1]
        i = map(str,i)
        i = ",".join(i)
        i = i + "\n"
        wf.write(i)
    wf.close()
    
get_whole_array()
    
#a = "/home/b/Documents/00490/Alex/csc490/data/parsed_accredited-2/proof vaccines dont cause autism/" 
#b = "/home/b/Documents/00490/Alex/csc490/data/accredited-2/"
#x = create_file(b,a)

#print "1" + 1