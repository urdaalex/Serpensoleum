from nltk.stem.lancaster import LancasterStemmer
from string import punctuation

'''
Notes on the implementation
    1) I inject a space between any punctuation and the last character
        before and after it - this is done in order for the stemmer to accurately
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

    # Get the paragraphs of the article & init a list of
    # new paragraphs (stemmed and processed versions of
    # old paragraphs)
    old_paragraphs = article_dict['paragraphs']
    new_paragraphs = []

    # Stem each paragraph and replace it with the unstemmed in
    # the article dictionary
    for i in range(len(old_paragraphs)):
        # Get the unstemmed paragraph
        unstemmed_paragraph = old_paragraphs[i]

        # Get the spaced out version of the unstemmed paragraph
        spaced_out = spaceOutTxt(unstemmed_paragraph)

        # Stem every item in the list split by spaces of the
        # spaced_out string
        stemmed_list = [st.stem(i) for i in spaced_out.split(' ')]

        # Construct the stemmed paragraph by adding the items
        # in the stemmed list together with spaces
        stemmed_paragraph = ''
        for i in stemmed_list[:-1]:
            stemmed_paragraph += i + ' '
        stemmed_paragraph += stemmed_list[-1]

        # Replace the unstemmed paragraph with the stemmed paragraph
        # in the paragraphs array
        new_paragraphs.append(stemmed_paragraph)

    article_dict['paragraphs'] = new_paragraphs

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
        for split_word in split_up[:-1]:
                new_txt += split_word + ' ' + punctuation[sofar]
        new_txt += split_up[-1]
        return spaceOutTxt(new_txt, sofar+1)

    else:
        return spaceOutTxt(txt, sofar+1)
