import json
import os
from measure_irrelevant import *

def load_document(path):
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def averagestuff(array):
    
    title = array[0]
    top1 = array[1]
    top5 = np.average(array[1:6])
    all_avg = np.average(array)
    
    return [title,top1,top5,all_avg]
    
def work_file(dir_file):
    '''
    get the (tfidf array,classification) for the file.
    0 = relevant
    1 = irrelevant
    '''

    doc = load_document(dir_file)
    query = doc['query'].lower()
    title = doc['title'].lower()
    body = doc['paragraphs']
    n_body = []
    for sen in body:
        #print type(sen)
        n_body.append(sen.lower())
    
    whole_article = [query] + [title] + n_body
    
    if doc['actual-search-type'] == "n":
        result = "n"
    else:
        result = "q"
    
    
    toreturn = averagestuff(get_tfidfsimilarity_matrix(whole_article))
    toreturn = toreturn + [result]
    return toreturn

def make_arff_file():
    towrite = []
    
    dirs = ["/home/b/Documents/00490/Alex/csc490/data/parsed/VA/1/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/2/proof vaccines dont cause autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/3/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/4/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/5/vaccines cause autism supporting evidence/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/6/proof vaccines cause autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/7/alkaline water cancer cure/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/8/alkaline water cancer cure -healthline/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/9/alkaline water cancer cure/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/10/black salve cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/11/black salve/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/12/black salve cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/13/cell phone cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/14/cell phone cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/15/cell phone cancer/"]
    
    g1 = ["/home/b/Documents/00490/Alex/csc490/data/parsed/VA/1/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/2/proof vaccines dont cause autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/3/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/4/vaccines AND autism/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/5/vaccines cause autism supporting evidence/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/VA/6/proof vaccines cause autism/"]
    
    g2 = ["/home/b/Documents/00490/Alex/csc490/data/parsed/7/alkaline water cancer cure/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/8/alkaline water cancer cure -healthline/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/9/alkaline water cancer cure/"]
    
    g3 = ["/home/b/Documents/00490/Alex/csc490/data/parsed/10/black salve cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/11/black salve/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/12/black salve cancer/"]
    
    g4 = ["/home/b/Documents/00490/Alex/csc490/data/parsed/13/cell phone cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/14/cell phone cancer/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/15/cell phone cancer/"]
    
    g5 = ["/home/b/Documents/00490/Alex/csc490/data/parsed/16/oral chelation heart disease/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/17/oral chelation heart disease/",
            "/home/b/Documents/00490/Alex/csc490/data/parsed/18/oral chelation heart disease/"]
    
    
    for single_dir in g4:
        
        files = os.listdir(single_dir)
        
        for ff in files:
            try:
                temp = work_file(single_dir+ff)
                temp = ",".join(map(str,temp))
                temp = temp + "\n"
                
                towrite.append(temp)
            except:
                print single_dir
            
    wf = open('test_train.txt','w')
    wf.write("".join(towrite))
    wf.close()
    
make_arff_file()