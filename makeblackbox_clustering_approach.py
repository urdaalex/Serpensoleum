import os
import sys
from html_parser import parse_document_tag_based

def main(argv):

    # The first arg is the path where the data folder is containing unprocessed
    # and unparsed JSON
    data_path = argv[0]

    # The second arg is the percentage of the data which will be used as
    # training data
    proportion_train = (float(argv[1]))/100
    proportion_test = 1 - percent_train

    # Get the full parsed data using the -tag method in html_parser.py
    all_data_parsed = getParsed(data_path)


def getParsed(data_path):
    '''
    Given the path to the folder containing all the data, this function
    parses all the data using the -tag method in html_parser.py
    '''
    

if __name__ == "__main__":
    main(sys.argv[1:])
