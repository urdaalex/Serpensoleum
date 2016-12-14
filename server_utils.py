from search_google import get_url
import IrrelevancyModule.NOV19.magic_function as irrelevancy_module
import TrueFalseModule.magic_function as tf_module
import html_parser as pars
import traceback
import os

ERROR_PARSING = 5
IRRELEVANT = 10


def classify_website(url, query):
    start = os.times()[0]

    try:
        contents = get_url(url)
    except:
        return ERROR_PARSING

    if contents == False:
        return ERROR_PARSING

    end = os.times()[0]

    print("Getting the webpage took:")
    print(end - start)

    start = os.times()[0]

    document_template = {"contents": contents, "query": query, "url": url}

    parsed_document = pars.parse_document_regex_based_sentences(document_template)[0]

    end = os.times()[0]
    print("Parsing the webpage took:")
    print(end - start)

    try:
        relevancy_result = irrelevancy_module.check_relevancy_of_document(parsed_document)
        if relevancy_result == True:
            return tf_module.tf_classifier(parsed_document)
        else:
            return IRRELEVANT
    except:
        traceback.print_exc()
        return ERROR_PARSING


def temp_test():
    contents = get_url('https://sharylattkisson.com/what-the-news-isnt-saying-about-vaccine-autism-studies/')

    document_template = {"contents": contents, "query": '', "url": 'https://sharylattkisson.com/what-the-news-isnt-saying-about-vaccine-autism-studies/'}

    parsed_document = pars.parse_document_regex_based_sentences(document_template)[0]

def pre_load_models():
    irrelevancy_module.pre_load_model('IrrelevancyModule/NOV19/saved_model.pkl')
    tf_module.pre_load_model('TrueFalseModule/nn_fancy_78_saved_model.pkl')
