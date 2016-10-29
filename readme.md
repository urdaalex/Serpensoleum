Dependencies:

1. pip install --upgrade google-api-python-client
2. pip install BeautifulSoup
3. pip install simplejson
4. pip install nltk
5. pip install --upgrade gensim


Usage:
```
search-google.py QUERY [FOLDER_NAME]
```

 * saves search results to json file: {url: "", content: ""}
```
categorize-results.py FOLDER_NAME
```
* takes all results in folder and opens URL in browser for you to categorize website (note: folder must have been create by search-google.py)
```
parser.py -method [INPUT_FOLDER_NAME] [OUTPUT_FOLDER_NAME]
```
* Iterates over all of the result files in the input folder, parses them to extract the text contents, and saves the results in the output folder. Note that a new folder is created within the output folder for each query. method can either be tag or regex.The format of the output files is: {'title': '', 'query': '', 'paragraphs': [], 'links': [], 'authors': []}
