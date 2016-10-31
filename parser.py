from bs4 import BeautifulSoup
from os import listdir
import sys
import os
import re
from os.path import isfile, join

import simplejson
import regex_helpers
import json

TAGS = ['span', 'div', 'par']


def main():
    """
    Running this function requires two command line arguments. The first argument is the input directory,
    the second argument is the output directory. The function reads every json file in the input directory,
    parses paragraphs, and stores an empty text file with the same corresponding name but different extension
    in the output directory.
    """
    if len(sys.argv) < 4 or not type(sys.argv[1]) is str or not type(sys.argv[2]) is str or not type(sys.argv[3]) is str:
        print "Incorrect number of args or args not of type string."
        print 'Correct usage is:'
        print 'python parser.py -method "input_dir_name" "output_dir_name"'
        print 'Where method is either regex or tag'
        print 'For example:: python parser.py -tag "raw" "parsed"'
        exit()

    method = sys.argv[1]
    input_directory = sys.argv[2]
    output_directory = sys.argv[3]

    if method == '-tag':
        parse_function = parse_document_tag_based
    elif method == '-regex_sent':
        parse_function = parse_document_regex_based_sentences
    elif method == '-regex_par':
        parse_function = parse_document_regex_based_paragraphs
    else:
        print 'Incorrect method: ' + method + ' specified.'
        print 'Please use one of the following flags:'
        print '-tag'
        print '-regex_sent'
        print '-regex_par'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    files = [f for f in listdir(input_directory) if isfile(join(input_directory, f)) and f.endswith('.json')]

    for f in files:
        document = load_document(os.path.join(input_directory, f))
        query = document['query']

        parsed_content = parse_function(document)

        if parsed_content is None:
            continue

        parsed_content['query'] = query

        if not os.path.exists(join(output_directory, query)):
            os.makedirs(join(output_directory, query))
        save_content(json.dumps(parsed_content), join(output_directory, query, f))


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

def parse_document_tag_based(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed based on HTML <p> tags. This has shown to be sufficient in some cases, though perhaps there are some
    edge cases where certain content might not be accessible by considering only <p> tags.

    :param document: A JSON object representing the result of a google search
    :return: A JSON object with the following schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website.
    """
    result = {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}

    # print whatisthis(document["contents"])
    soup = BeautifulSoup(document['contents'], 'html.parser')

    pars = soup.find_all('p')

    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href != None:
            result['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        result['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        h1s = soup.select('h1')
        for h1 in h1s:
            result['title'] = h1.get_text().encode('ascii', 'ignore')
            break

    num_words = 0

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
        if (len(text.split(" ")) > 5):
            if not regex_helpers.check_text_for_garbage(text.lower(), regex_helpers.GARBAGE) and \
                regex_helpers.check_ends_with_punctuation(text):
                text = re.sub('\s+', ' ', text)
                # print text
                # print ""
                num_words += len(text.split(' '))
                result['paragraphs'].append(text)
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

    if num_words < 100:
        return None

    return result

def parse_document_regex_based_paragraphs(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed all HTML tags that are children of <body>. However, tags like <script> are ignored. This allows for a
    more liberal

    :param document: A JSON object representing the result of a google search
    :return: A JSON object with the following schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website.
    """
    result = {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}

    soup = BeautifulSoup(document['contents'], 'html.parser')

    body = soup.select("body *")

    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href != None:
            result['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        result['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        h1s = soup.select('h1')
        for h1 in h1s:
            result['title'] = h1.get_text().encode('ascii', 'ignore')
            break

    generator = (element for element in body if element.name != 'script' and element.name != 'img' and len(element.findChildren()) == 0)

    num_words = 0

    for element in generator:
        text = element.get_text().encode('ascii', 'ignore')

        sentences = re.split(regex_helpers.PARAGRAPH_SPLITTING_PATTERN, text)

        paragraph = ""

        for sentence in sentences:
            trimmed = re.sub('\s+', ' ', sentence)
            if trimmed != '' and regex_helpers.check_ends_with_punctuation(trimmed) and not \
                    regex_helpers.check_text_for_garbage(trimmed, regex_helpers.GARBAGE):
                paragraph += ' ' + trimmed

        if paragraph != "" and len(paragraph.split(' ')) > 5 :
            result['paragraphs'].append(paragraph)
            # print paragraph
            # print ""
            num_words += len(paragraph.split(' '))

    if num_words < 150:
        return None

    return result

def parse_document_regex_based_sentences(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed all HTML tags that are children of <body>. However, tags like <script> are ignored. This allows for a
    more liberal

    :param document: A JSON object representing the result of a google search
    :return: A JSON object with the following schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website.
    """
    result = {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}

    soup = BeautifulSoup(document['contents'], 'html.parser')

    body = soup.select("body *")

    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href != None:
            result['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        result['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        h1s = soup.select('h1')
        for h1 in h1s:
            result['title'] = h1.get_text().encode('ascii', 'ignore')
            break

    generator = (element for element in body if element.name != 'script' and element.name != 'img' and len(element.findChildren()) == 0)

    num_words = 0

    for element in generator:
        text = element.get_text().encode('ascii', 'ignore')

        sentences = re.split(regex_helpers.PARAGRAPH_SPLITTING_PATTERN, text)

        for sentence in sentences:
            trimmed = re.sub('\s+', ' ', sentence)
            len_trimmed = len(trimmed)
            if trimmed != '' and regex_helpers.check_ends_with_punctuation(trimmed) and not \
                    regex_helpers.check_text_for_garbage(trimmed, regex_helpers.GARBAGE) and \
                    len_trimmed > 5:
                result['paragraphs'].append(trimmed)
                num_words += len_trimmed

    if num_words < 150:
        return None

    return result

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return True
    return False



if __name__ == "__main__":
    main()