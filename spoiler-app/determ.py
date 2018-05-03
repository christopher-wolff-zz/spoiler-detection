#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import cgi
from collections import OrderedDict
from operator import itemgetter
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from urllib.parse import parse_qs, urlparse

mnb = pickle.load(open('./mnb.pkl', 'rb'))
vec = pickle.load(open('./vec.pkl', 'rb'))

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        pass
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
        self._set_response()
        index = post_data.find('data=')
        review_text = str(post_data[index + 5:].replace('%20', ' '))
        v = CountVectorizer(vocabulary=vec.vocabulary_)
        x = [review_text]
        x_in = v.fit_transform(x)
        y = mnb.predict_proba(x_in)
        self.wfile.write(str(y[0][1]).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
