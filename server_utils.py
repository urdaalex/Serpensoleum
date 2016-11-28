from search_google import get_url
import sys
from IrrelevancyModule.NOV19.magic_function import check_relevancy_of_document
# sys.path.insert(0, 'IrrelevancyModule/NOV19/')
# from magic_function import *
# from IrrelevancyModule.NOV19.magic_function import magic_function
import html_parser as pars
import traceback
import os
import numpy as np

ERROR_PARSING = 5

def check_website_relevancy(url, query):
    # if not url.startswith('http'):
    #     new_url = 'http://' + url
    #
    #     try:
    #         contents = get_url(new_url)
    #         print("------------------------------Tried Adding http://------------------------------")
    #         print("To: " + url)
    #     except:
    #         new_url = 'https://' + url
    #         print("------------------------------Tried Adding https://------------------------------")
    #         print("To: " + url)
    #         contents = get_url(new_url)
    # else:
    #     print("------------------------------Didn't add anything------------------------------")
    try:
        contents = get_url(url)
    except:
        return ERROR_PARSING

    if contents == False:
        return ERROR_PARSING

    document_template = {"contents": contents, "query": query, "url": url}

    parsed_document = pars.parse_document_regex_based_sentences(document_template)[0]

    print("-------------------------request start-------------------------")
    print("query: " + query)
    print("url: " + url)
    print("first 10 chars of contents: " + contents[:9])
    print("parsed_doc: " + str(parsed_document.keys()))
    print("-------------------------request end-------------------------")

    try:
        relevancy_result = check_relevancy_of_document(parsed_document, 'IrrelevancyModule/NOV19/saved_model.pkl')
        return relevancy_result
    except:
        traceback.print_exc()
        return ERROR_PARSING

def check_website_validity():
    return False
# def magic_function(doc):
#     x = np.random.rand(1,1)
#
#     if x <= 0.5:
#         return False
#     else:
#         return True