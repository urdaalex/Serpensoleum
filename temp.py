import pprint
import sys
import urllib2
import os
import json
import webbrowser

FOLDER = "./" + sys.argv[1] + "/"
VALID_CATEGORIES = ['f', 'a', 'u', 'n', 't']
def main():
	i=1
	for fn in listdir_path(FOLDER):
		print("\n" + str(i) + "/" + str(len(listdir_path(FOLDER))))
		i = i + 1

		doc = load_document(fn)

		#if doc was already categorized, skip
		if('expected-search-type' in doc):
			if(doc['actual-search-type']=='a'):
				doc['actual-search-type'] = 't'

		save_content(json.dumps(doc), fn)	

		
def listdir_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]



def load_document(path):
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def save_content(content, path):
  f = open(path, 'w')
  f.write(content)
  f.close()

if __name__ == '__main__':
  main()