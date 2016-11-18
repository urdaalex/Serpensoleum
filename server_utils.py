from search_google import get_url
import html_parser as pars
import numpy as np

def check_website_truthfullness(url, query):
    if not url.startswith('http'):
        new_url = 'http://' + url

        try:
            contents = get_url(new_url)
            print("------------------------------Tried Adding http://------------------------------")
            print("To: " + url)
        except:
            new_url = 'https://' + url
            print("------------------------------Tried Adding https://------------------------------")
            print("To: " + url)
            contents = get_url(new_url)
    else:
        print("------------------------------Didn't add anything------------------------------")
        contents = get_url(url)

    document_template = {"contents": contents, "query": query, "url": url}

    parsed_document = pars.parse_document_regex_based_sentences(document_template)

    # parsed_document = None
    return magin_function(parsed_document)

def magin_function(parsed_document):
    return True
