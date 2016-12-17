import os
import sys

def main(argv):

    # The first arg is the path where the data folder is containing unprocessed
    # and unparsed JSON
    data_path = argv[0]

    # The second arg is the percentage of the data which will be used as
    # training data
    proportion_train = (float(argv[1]))/100
    proportion_test = 1 - proportion_train

    # Get the full parsed data using the -tag method in html_parser.py
    folder_with_parsed = getParsed(data_path)


def getParsed(data_path):
    '''
    Given the path to the folder containing all the data, this function
    parses all the data using the -tag method in html_parser.py
    '''
    parsed_data_name = 'parsed_' + data_path
    unorg_folder_name = "unorganized_" + parsed_data_name

    if os.path.exists(parsed_data_name):
        if os.path.exists(unorg_folder_name):
            print unorg_folder_name + " exists prior to execution"
        else:
            os.system("python getAllUnorganized.py " + parsed_data_name + " " + unorg_folder_name)
        return unorg_folder_name

    os.system("python html_parser.py -tag " + data_path + " " + parsed_data_name)
    os.system("python getAllUnorganized.py " + parsed_data_name + " " + unorg_folder_name)
    return unorg_folder_name

if __name__ == "__main__":
    main(sys.argv[1:])
