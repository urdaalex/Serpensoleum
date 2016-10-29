Dependencies:
pip install --upgrade google-api-python-client

pip install BeautifulSoup


Usage:
```
search-google.py QUERY [FOLDER_NAME]
```

 * saves search results to json file: {url: "", content: ""} 
```
categorize-results.py FOLDER_NAME
```
* takes all results in folder and opens URL in browser for you to categorize website
