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
import _pickle as cPickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import spacy
from spacy import displacy
from spacy.symbols import nsubj, nsubjpass, VERB
import en_core_web_sm
from urllib.parse import parse_qs, urlparse

nlp = en_core_web_sm.load()
nlp.add_pipe(nlp.create_pipe('sentencizer'))

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
        self._set_response()
        index = post_data.find('data=')
        review_text = str(post_data[index + 5:].replace('%20', ' '))
        pairs = []
        print(review_text)
        doc = nlp(review_text)
        for k, sentence in enumerate(doc.sents):
            for token in sentence:
                print(token)
                print(token.dep_)
                if (token.dep == nsubj or token.dep == nsubjpass) and token.head.pos == VERB:
                    compounds = [child.lower_ for child in token.children if child.dep_ == 'compound']
                    compounds.append(token.lower_)
                    pairs.append('-'.join(compounds) + '|' + token.head.lemma_.lower())
        subj_verb = ', '.join(pairs)

        x = [subj_verb]
        print(x)

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
