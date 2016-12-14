from bs4 import BeautifulSoup
from os import listdir
import sys
import os
import re
from os.path import isfile, join

import regex_helpers
import string_helpers as sh
import json
import nltk.data

TAGS = ['span', 'div', 'par']


def main():
    """
    Running this function requires two command line arguments. The first argument is the input directory,
    the second argument is the output directory. The function reads every json file in the input directory,
    parses paragraphs, and stores an empty text file with the same corresponding name but different extension
    in the output directory.
    """
    if len(sys.argv) < 4 or not type(sys.argv[1]) is str or not type(sys.argv[2]) is str or not type(
            sys.argv[3]) is str:
        print "Incorrect number of args or args not of type string."
        print 'Correct usage is:'
        print 'python html_parser.py -method "input_dir_name" "output_dir_name"'
        print 'Where method is either regex or tag'
        print 'For example:: python html_parser.py -tag "raw" "parsed"'
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
        exit()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    files = [f for f in listdir(input_directory) if isfile(join(input_directory, f)) and f.endswith('.json')]

    for f in files:
        document = load_document(os.path.join(input_directory, f))
        query = document['query']

        print 'Parsed: ' + document['url']
        print ""

        parsed_content, parsed_status = parse_function(document)

        if parsed_status == False:
            print 'Ignored: ' + document['url']
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


def parse_document_tag_based(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed based on HTML <p> tags. This has shown to be sufficient in some cases, though perhaps there are some
    edge cases where certain content might not be accessible by considering only <p> tags.

    :param document: A JSON object representing the result of a google search
    :return: A  tuple of the form (JSON object, boolean)
    JSON object has the following additional properties added to the
    input: schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website. The boolean represents whether or not the document has more than
    150 words.
    """
    document['authors'] = []
    document['links'] = []
    document['paragraphs'] = []

    soup = BeautifulSoup(document['contents'], 'html.parser')

    pars = soup.find_all('p')

    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href != None:
            document['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        document['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        h1s = soup.select('h1')
        for h1 in h1s:
            document['title'] = h1.get_text().encode('ascii', 'ignore')
            break

    num_words = 0
    num_pars = 0

    for element in pars:
        images = element.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')
        for image in images:
            image.clear()
        text = element.get_text().encode('ascii', 'ignore')

        if (len(text.split(" ")) > 5):
            if not regex_helpers.check_text_for_garbage(text.lower(), regex_helpers.GARBAGE) and \
                    regex_helpers.check_ends_with_punctuation(text):
                text = re.sub('\s+', ' ', text)
                text = text.replace('"', '')
                num_pars += 1
                num_words += len(text.split(' '))
                document['paragraphs'].append(text)

    if num_words < 100:
        return document, False

    return document, True


def parse_document_regex_based_paragraphs(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed all HTML tags that are children of <body>. However, tags like <script> are ignored. This allows for a
    more liberal

    :param document: A JSON object representing the result of a google search
    :return: A  tuple of the form (JSON object, boolean)
    JSON object has the following additional properties added to the
    input: schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website. The boolean represents whether or not the document has more than
    150 words.
    """
    document['authors'] = []
    document['links'] = []
    document['paragraphs'] = []

    soup = BeautifulSoup(document['contents'], 'html.parser')

    body = soup.select("body *")
    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href is not None:
            document['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        document['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        h1s = soup.select('h1')
        for h1 in h1s:
            document['title'] = h1.get_text().encode('ascii', 'ignore')
            break

    generator = (element for element in body if
                 element.name != 'script' and element.name != 'img' and len(element.findChildren()) == 0)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    num_words = 0
    num_pars = 0

    for element in generator:
        text = element.get_text().encode('ascii', 'ignore')

        sentences = tokenizer.tokenize(text)
        paragraph = ""

        for sentence in sentences:
            sentence = sh.remove_garbage(sentence)

            if sentence != '' and regex_helpers.check_ends_with_punctuation(sentence) and not \
                    regex_helpers.check_text_for_garbage(sentence, regex_helpers.GARBAGE):
                paragraph += ' ' + sentence

        paragraph.replace(' ', '', 1)

        if paragraph != "" and len(paragraph.split(' ')) > 5:
            document['paragraphs'].append(paragraph)
            num_pars += 1
            num_words += len(paragraph.split(' '))

    if num_words < 150:
        return document, False

    return document, True


def parse_document_regex_based_sentences(document):
    """
    Takes in a JSON object representing an HTML page, accesses its 'contents' tag, and parses the content. The content
    is parsed all HTML tags that are children of <body>. However, tags like <script> are ignored. This allows for a
    more liberal

    :param document: A JSON object representing the result of a google search
    :return: A  tuple of the form (JSON object, boolean)
    JSON object has the following additional properties added to the
    input: schema {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
    representing the parsed contents of a website. The boolean represents whether or not the document has more than
    150 words.
    """
    document['authors'] = []
    document['links'] = []
    document['paragraphs'] = []

    soup = BeautifulSoup(document['contents'], 'html.parser')
    if 'cdc' in document['query']:
        print

    body = soup.select("body *")
    links = soup.find_all('a')
    images = soup.select('a[class*="image"], a[class*="pict"], a[class*="phot"]')

    links = [link for link in links if link not in images]

    for link in links:
        href = link.get('href')
        if href != None:
            document['links'].append(href.encode('ascii', 'ignore'))

    if soup.title:
        document['title'] = soup.title.get_text().encode('ascii', 'ignore')
    else:
        title = soup.select('head title')

        if title is not None:
            for t in title:
                document['title'] = t.get_text().encode('ascii', 'ignore')
                break
        else:
            h1s = soup.select('h1')
            for h1 in h1s:
                document['title'] = h1.get_text().encode('ascii', 'ignore')
                break

    generator = (element for element in body if
                 element.name != 'script' and element.name != 'img' and len(element.findChildren()) == 0)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    num_words = 0

    for element in generator:
        text = element.get_text().encode('ascii', 'ignore')

        sentences = tokenizer.tokenize(text)

        for sentence in sentences:
            sentence = sh.remove_garbage(sentence)
            len_sentence = len(sentence.split(' '))

            if sentence != '' and regex_helpers.check_ends_with_punctuation(sentence) and not \
                    regex_helpers.check_text_for_garbage(sentence, regex_helpers.GARBAGE) and \
                            len_sentence > 5:
                document['paragraphs'].append(sentence)
                num_words += len_sentence

    if document['paragraphs'] == []:
        body = soup.select('*')
        generator = (element for element in body if
                     element.name != 'script' and element.name != 'img' and len(element.findChildren()) == 0)

        for element in generator:
            text = element.get_text().encode('ascii', 'ignore')

            sentences = tokenizer.tokenize(text)

            for sentence in sentences:
                sentence = sh.remove_garbage(sentence)
                len_sentence = len(sentence.split(' '))

                if sentence != '' and regex_helpers.check_ends_with_punctuation(sentence) and not \
                        regex_helpers.check_text_for_garbage(sentence, regex_helpers.GARBAGE) and \
                                len_sentence > 5:
                    document['paragraphs'].append(sentence)
                    num_words += len_sentence

    if num_words < 150:
        return document, False

    return document, True


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return True
    return False


if __name__ == "__main__":
    main()
