from bs4 import BeautifulSoup
from os import listdir
import sys
import os
from os.path import isfile, join

import simplejson
import json

TAGS = ['span', 'div', 'par']


def main():
    """
    Running this function requires two command line arguments. The first argument is the input directory,
    the second argument is the output directory. The function reads every json file in the input directory,
    parses paragraphs, and stores an empty text file with the same corresponding name but different extension
    in the output directory.
    """
    if len(sys.argv) < 3 or not type(sys.argv[1]) is str or not type(sys.argv[2]) is str:
        print "Incorrect number of args or args not of type string."
        print 'Correct usage is:'
        print 'python parser.py "input_dir_name" "output_dir_name"'
        exit()

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    files = [f for f in listdir(input_directory) if isfile(join(input_directory, f)) and f.endswith('.json')]

    for f in files:
        document = load_document(os.path.join(input_directory, f))
        result = parse_document(document)
        save_content(result, join(output_directory, f.strip('.json') + '.txt'))


def load_document(path):
    with open(path) as json_data:
        document = json.load(json_data)
    return document

def save_content(content, path):
  f = open(path, 'w')
  f.write(content)
  f.close()

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"

def parse_document(document):
    result = ''
    # print whatisthis(document["contents"])
    soup = BeautifulSoup(document['contents'], 'html.parser')

    pars = soup.find_all('p')

    for element in pars:
        # if not any(True for _ in element.children):
        # for child in element.children:
        #     print child.get_text().encode('utf-8')

        images = element.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')
        # images.clear()
        for image in images:
            image.clear()
        text = element.get_text().encode('ascii', 'ignore')

        # print element

        # for child in element.children:
        #     if child.name == "img":
        #         child.clear()
        if (len(text.split(" ")) > 7):
            result += text
            result += '\n\n'
            print text
            print ''
        # print element.contents
    # for tag in TAGS:
    #     for tag1 in TAGS:
    #         relevant = soup.select(tag + " " + tag1)
    #         print relevant

    # for par in pars:
    #     print par
    #
    # text = soup.get_text()
    # print text.encode('utf-8')

    return result


if __name__ == "__main__":
    main()