#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""



import pprint

from googleapiclient.discovery import build


API_KEY = "AIzaSyB-HfmAFqW10Hp3nO7Vh6MX2s7LDMvRdAg"
CSE_ID = "017448297487401808077:o0oyzopipio"
QUERY = "lectures"

NUM_OF_PAGES = 1

def main():
  service = build("customsearch", "v1",
            developerKey=API_KEY)


  for curr_page in range(0,NUM_OF_PAGES):

    res = service.cse().list(
        q=QUERY,
        cx=CSE_ID,
        start=(curr_page*10 + 1),
      ).execute()

    if not 'items' in res:
        print 'No result !!\nres is: {}'.format(res)
    else:
        for item in res['items']:
            print('{}:\n\t{}'.format(item['title'], item['link']))


if __name__ == '__main__':
  main()