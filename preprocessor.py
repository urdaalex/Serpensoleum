from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation

'''
Notes on the implementation
    1) I inject a space between any punctuation and the last character
        before and after it - this is done in order for the stemmer to accurately
        be able to stem the word. If we have x = 'maximum?' and we try
        to stem x, we'll get x back unaltered. If, however, x = 'maximum',
        then stemming x will yield 'maxim' which is what we want.
'''

def getProcessedDocument(article_dict):
    '''
    Given a dictionary in format returned from parser.py, this function
    replaces the paragraphs in the paragraphs list (i.e. the body of
    the parsed article) with the stemmed version of those paragraphs
    (using the Lancaster Stemming Algorithm), and removes the stop
    words in the paragraphs.
    '''
    # Init the stemmer
    st = LancasterStemmer()

    # Init a list of new paragraphs (processed versions of
    # old paragraphs)
    new_paragraphs = []

    # Stem each paragraph and replace it with the unstemmed in
    # the article dictionary
    for unprocessed_paragraph in article_dict['paragraphs']:
        # Get the spaced out version of the unprocessed paragraph
        spaced_out = spaceOutTxt(unprocessed_paragraph)

        # Remove all stop words from spaced out paragraph
        without_stopwords = removeStopWords(spaced_out)

        # Apply Lancaster Stemming
        stemmed_paragraph = stemTxt(without_stopwords, st)

        # Add the processed paragraph to the new paragraphs list
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

def removeStopWords(txt):
    '''
    Given a string input 'txt', this function removes all
    occurences of stop words in the text
    '''
    # Filter out the stop words
    filtered = [word for word in txt.split(' ') if word not in stopwords.words('english')]

    # Reconstruct & return the string from the filtered list
    txt = ''
    for word in filtered[:-1]:
        txt += word + ' '
    return txt + filtered[-1]

def stemTxt(txt, st):
    '''
    Given a string input 'txt', this function applies stems the input
    using the stemmer specified by 'st'.
    '''
    # Stem the words in the txt
    stemmed_list = [st.stem(i) for i in txt.split(' ')]

    # Reconstruct & return the string from the stemmed list
    stemmed_paragraph = ''
    for i in stemmed_list[:-1]:
        stemmed_paragraph += i + ' '
    return stemmed_paragraph + stemmed_list[-1]
