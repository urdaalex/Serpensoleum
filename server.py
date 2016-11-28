import web
import json
from server_utils import *

urls = ('/check_valid', 'MyServer')

class MyServer(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('127.0.0.1', port))

    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        data = json.loads(web.data())
        # print("-------------------------request start-------------------------")
        # print("query: " + data['query'])
        # print("-------------------------request end-------------------------")

        url = data['url']
        query = data['query']

        return relevancy_handler(query, url)


        # return 'URL sent was: ' + value

def relevancy_handler(query, url):
    response = {'relevant': False}
    truthfulness = check_website_relevancy(url, query)

    if truthfulness == ERROR_PARSING:
        response['error'] = 'Error Parsing'
    else:
        response['relevant'] = truthfulness
    return json.dumps(response)


def classification_handler(query, url):
    response = {'valid': False}
    truthfulness = check_website_validity(url, query)

    if truthfulness == ERROR_PARSING:
        response['error'] = 'Error Parsing'

    if check_website_validity(url, query):
        response['valid'] = truthfulness
        return json.dumps(response)
    else:
        return json.dumps(response)


if __name__ == '__main__':
    app = MyServer(urls, globals())
    app.run(port=3000)













# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
# import simplejson
# import random
#
# class S(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#         f = open("index.html", "r")
#         self.wfile.write(f.read())
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     def do_POST(self):
#         self._set_headers()
#         print "in post method"
#         self.data_string = self.rfile.read(int(self.headers['Content-Length']))
#
#         self.send_response(200)
#         self.end_headers()
#
#         data = simplejson.loads(self.data_string)
#         with open("test123456.json", "w") as outfile:
#             simplejson.dump(data, outfile)
#         print "{}".format(data)
#         f = open("for_presen.py")
#         self.wfile.write(f.read())
#         return
#
#
# def run(server_class=HTTPServer, handler_class=S, port=5000):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print 'Starting httpd...'
#     httpd.serve_forever()
#
# if __name__ == "__main__":
#     from sys import argv
#
# if len(argv) == 2:
#     run(port=int(argv[1]))
# else: