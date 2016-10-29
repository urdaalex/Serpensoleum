import pprint
import sys
import urllib2
import os
import json
import webbrowser

FOLDER = "./" + sys.argv[1] + "/"
VALID_CATEGORIES = ['f', 'a', 'u', 'n']
def main():
	print("Enter the category of this search (don't pick 'q') ")
	expected = get_expected_category()

	for fn in listdir_path(FOLDER):
		print("")
		doc = load_document(fn)

		#if doc was already categorized, skip
		if('expected-search-type' in doc):
			print(fn + " was already categorized...skipping")
			continue

		open_url(doc['url'])

		response = get_category()

		#if response was 'q', skip 
		if(response=='q'):
			continue

		doc['expected-search-type'] = expected
		doc['actual-search-type'] = response

		save_content(json.dumps(doc), fn)	

		
def listdir_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def open_url(url):
	print("Opening " + url)
	webbrowser.open(url, new=2, autoraise=False)

def get_expected_category():
	res = raw_input("Input: [f]ake, [a]ccredited. [u]nbiased \t")
	
	while (res not in VALID_CATEGORIES):
		res = raw_input("Incorrect input...choose [f]ake, [a]ccredited. [u]nbiased  \t")

	return res


def get_category():
	res = raw_input("Input: [f]ake, [a]ccredited, [n]ot relevant. q to skip \t")
	
	while (res not in VALID_CATEGORIES and res != "q"):
		res = raw_input("Incorrect input...choose [f]ake, [a]ccredited, [n]ot relevant. q to skip \t")

	return res


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