from nltk.stem.lancaster import LancasterStemmer
import re
from string import punctuation

'''
Notes on the implementation
    1) I inject a space between any punctuation and the last character
        before it - this is done in order for the stemmer to accurately
        be able to stem the word. If we have x = 'maximum?' and we try
        to stem x, we'll get x back unaltered. If, however, x = 'maximum',
        then stemming x will yield 'maxim' which is what we want.
'''

def getStemmedDocument(article_dict):
    '''
    Given a dictionary in format returned from parser.py, this function
    replaces the paragraphs in the paragraphs list (i.e. the body of
    the parsed article) with the stemmed version of those paragraphs
    (using the Lancaster Stemming Algorithm)
    '''
    # Init the stemmer
    st = LancasterStemmer()

    # Get the paragraphs of the article
    paragraphs = article_dict['paragraphs']

    # Stem each paragraph and replace it with the unstemmed in
    # the article dictionary
    for i in range(len(paragraphs)):
        unstemmed_paragraph = paragraphs[i]
        spaced_out = spaceOutTxt(unstemmed_paragraph)
        pass

def spaceOutTxt(txt, sofar=0):
    '''
    Given txt that may or may not have punctuation, this
    function adds a space between punctuation and the character
    attached to it on either side
    '''
    if(sofar == len(punctuation)-1):
        return txt
    if(punctuation[sofar] in txt):
        split_up = txt.split(punctuation[sofar])
        new_txt = ''
        for i in range(len(split_up)):
            split_word = split_up[i]
            if(i != len(split_up)-1):
                new_txt += split_word + ' ' + punctuation[sofar]
            else:
                new_txt += split_word
        return spaceOutTxt(new_txt, sofar+1)
    else:
        return spaceOutTxt(txt, sofar+1)
