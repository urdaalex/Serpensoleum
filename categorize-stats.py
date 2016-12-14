#Given a folder, it prints count of expected + actual results
#Example Usage:   python scriptName.py DIR
#Example Result:  Expected 54 Accredited; Got 5 Accredit, 6 False, 10 Unrelated

import json
import sys
import os 

FOLDER = "./" + sys.argv[1] + "/"
cat_dictionary = {"t":0,"n":0,"f":0}

def load_document(path):
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def listdir_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def main():
    true = None
    group = None
    counter = 0
    for fn in listdir_path(FOLDER):
	doc = load_document(fn)
	cat_dictionary[doc["actual-search-type"]] = cat_dictionary[doc["actual-search-type"]] + 1
	counter += 1
	if true is None:
	    true = doc["expected-search-type"]
	    if true == "t":
		group = "True"
	    elif true == "f":
		group = "False"
	    elif true == "n":
		group = "Not Relevant"
	    elif true == "u":
		group = "Unbiased"
	 
    print("Expected "+str(counter)+" "+group+"; Got "+str(cat_dictionary["t"])+" True, "+str(cat_dictionary["f"])+" False, "+str(cat_dictionary["n"])+" Unrelated")

if __name__ == "__main__":
    main()