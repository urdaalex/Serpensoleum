"""
A tool that searches for classified websites that were classified more than once.
Developed to find the interhuman analysis kappa value, as we need to use sites that were 
overlapped between raters.

Usage: python NAME.py DIR

"""

import pprint
import sys
import urllib2
import os
import json
import webbrowser

FOLDER = "./" + sys.argv[1] + "/"
def main():
	#build dictionary
	d = {}

	for fn in listdir_path(FOLDER):
		doc = load_document(fn)

		#if doc was already categorized, skip
		if(not 'actual-search-type' in doc):
			print("not categorized")
			continue

		if(not doc['url'] in d.keys()):
			if(doc['actual-search-type']=='t'):
				d[doc['url']] =[1,0,0]
			if(doc['actual-search-type']=='f'):
				d[doc['url']] =[0,1,0]
			if(doc['actual-search-type']=='n'):
				d[doc['url']] =[0,0,1]
		else:
			if(doc['actual-search-type']=='t'):
				d[doc['url']][0] = d[doc['url']][0]	+ 1
			if(doc['actual-search-type']=='f'):
				d[doc['url']][1] = d[doc['url']][1]	+ 1
			if(doc['actual-search-type']=='n'):
				d[doc['url']][2] = d[doc['url']][2]	+ 1

	for k,v in d.iteritems():
		if (v[0] + v[1] + v[2] > 1):
			print(" [t,f,n]:" + str(v))
		
def listdir_path(d):
    '''
    Given a directory list all of the files in given directory

    Attributes:
        d (str): path to a directory.
    '''
    return [os.path.join(d, f) for f in os.listdir(d)]


def load_document(path):
    '''
    Given a path to a JSON file, the json object is returned
    
    Attributes:
        path (str): Path to JSON file
    '''
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def save_content(content, path):
  f = open(path, 'w')
  f.write(content)
  f.close()

if __name__ == '__main__':
  main()
