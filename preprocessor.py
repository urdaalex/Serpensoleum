from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from string import punctuation
import simplejson
import sys
import os

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

    return new_paragraphs

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
        new_txt += ' ' split_up[-1]
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
    Given a string input 'txt', this function stems the input
    using the stemmer specified by 'st'.
    '''
    # Stem the words in the txt
    stemmed_list = [st.stem(i) for i in txt.split(' ')]

    # Reconstruct & return the string from the stemmed list
    stemmed_paragraph = ''
    for i in stemmed_list[:-1]:
        stemmed_paragraph += i + ' '
    return stemmed_paragraph + stemmed_list[-1]

def validInputs(input_list):
    '''
    Given the list of input arguments, this function will return a boolean
    indicating whether or not the inputs are valid
    '''
    proper_usage = "Incorrect number of args or input dir does not exist or output dir already exists\n" +\
                "Correct usage: \n" +\
                "\t python preprocessor.py 'input_dir_name' 'output_dir_name'"

    if (len(input_list) != 2 or not os.path.exists(input_list[0]) or os.path.exists(input_list[1])):
        print proper_usage
        return False

    return True

def main(argv):
    '''
    Given the array of arguments to the program, the main method will ensure
    that the inputs are valid, if they are, the JSON files in the input
    directory will be loaded, and fully preprocessed. The processed
    JSON files will then be saved to the output directory specified by the
    input arguments
    '''
    # Check if the input arguments are valid
    if not validInputs(argv):
        sys.exit(1)

    # Load a list of the JSON files in the input dir
    JSON_files = []
    for filename in os.listdir(argv[0]):
        with open(argv[0] + filename, 'r') as json_file:
            JSON_files.append((filename, simplejson.load(json_file)))

    # Process the paragraphs in the JSON files
    for (filename,unprocd_json) in JSON_files:
        unprocd_json['paragraphs'] = getProcessedDocument(unprocd_json)

    # Dump the new json files in the output directory
    os.makedirs(argv[1])
    for (filename, procd_json) in JSON_files:
        with open(argv[1] + "/" + filename, "w") as out_file:
            simplejson.dump(procd_json, out_file)

if __name__ == "__main__":
    main(sys.argv[1:])
