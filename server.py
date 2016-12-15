import web
import json
from server_utils import *

urls = ('/check_valid', 'MyServer')
IRRELEVANT = 10


class MyServer(web.application):
    def run(self, port=8080, *middleware):
        '''Run the server.
        
        Args:
            self (MyServer): Takes in a server object.
            port (int): Which port should the server be run on.
        '''
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('127.0.0.1', port))

    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        data = json.loads(web.data())

        url = data['url']
        query = data['query']

        return classification_handler(query, url)


def classification_handler(query, url):
    response = {}
    truthfulness = classify_website(url, query)


    if truthfulness == IRRELEVANT:
        response['relevant'] = False
    elif truthfulness == ERROR_PARSING:
        response['error'] = 'Error Parsing'
    else:
        response['validity'] = truthfulness
    return json.dumps(response)


if __name__ == '__main__':
    pre_load_models()
    app = MyServer(urls, globals())
    app.run(port=3000)
