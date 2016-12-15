"""Simple command-line example for Custom Search.
Command-line application that does a search.

Usage: search-python QUERY [OUTPUT_FOLDER]
Note: change the CSE_ID variable to use different search filters
"""


import cookielib
import pprint
import sys
import urllib2
import os
import json
import traceback

from googleapiclient.discovery import build


API_KEY = "AIzaSyB-HfmAFqW10Hp3nO7Vh6MX2s7LDMvRdAg"

CSE_ID = "017448297487401808077:o0oyzopipio" #search all sites
#CSE_ID = "017448297487401808077:uw5linhdq6c" #schema.org limitation [MedicalEntity] - all sites
#CSE_ID = "017448297487401808077:wklbk_lctfa" #blogs only
#CSE_ID = "017448297487401808077:wnqqxbff81o" #HONCode replica

QUERY = ""

if len(sys.argv) != 3:
  DOWNLOAD_FOLDER="./raw/"
else:
  DOWNLOAD_FOLDER= "./" + sys.argv[2] + "/"

NUM_OF_PAGES = 3

def main():
  global QUERY
  QUERY = sys.argv[1]
  service = build("customsearch", "v1",
            developerKey=API_KEY)

  if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

  for curr_page in range(0,NUM_OF_PAGES):
    starting_index = curr_page*10 + 1

    res = service.cse().list(
        q=QUERY,
        cx=CSE_ID,
        start=starting_index,
      ).execute()



    if not 'items' in res:
        print 'Error: No result !!\nres is: {}'.format(res)
    else:
        for item in res['items']:
            print(item['link'])
            content = get_url(item['link'])
            if(not content):
              print("***Could not retreive above site, skipping***")
            else:
              json_content = {}
              json_content['url'] = item['link']
              json_content['query'] = QUERY
              json_content['contents'] = content

              try:
                save_content(json.dumps(json_content), DOWNLOAD_FOLDER+"{} - {} [{}].json".format(QUERY, starting_index, item['displayLink']))
              except UnicodeDecodeError as e:
                print("**********ERROR DECODING, skipping above url****************\n\n")
            starting_index += 1


def get_url(url):
  print('Get url ' + url)
  fake_hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
  req = urllib2.Request(url, headers=fake_hdr)
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  try:
    # res = urllib2.urlopen(req, timeout=5)
    res = opener.open(req, timeout=5)
    content = res.read()
    return content

  except urllib2.URLError as e:
    traceback.print_exc()
    return False
  except:
    traceback.print_exc()
    return False

def save_content(content, path):
  f = open(path, 'w')
  f.write(content)
  f.close()


if __name__ == '__main__':
  main()