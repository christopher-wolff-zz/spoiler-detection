from collections import OrderedDict
from operator import itemgetter
import pandas as pd
import numpy as np
import sys
import _pickle as cPickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from scipy.sparse import hstack
import spacy
from spacy import displacy
from spacy.symbols import nsubj, nsubjpass, VERB
import en_core_web_sm
import cherrypy

class HelloWorld(object):
    nlp = en_core_web_sm.load()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    subj_verbs = list()

    print("YEET")
    sys.stdout.flush()
    def apple():
        print("aplpe")
        return 8
    
cherrypy.quickstart(HelloWorld())