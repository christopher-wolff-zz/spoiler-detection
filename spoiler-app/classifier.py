from collections import OrderedDict
from operator import itemgetter
import pandas as pd
import numpy as np
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

nlp = en_core_web_sm.load()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


reviews = pd.read_csv('../data/reviews_tempV3.csv', usecols=['review_id', 'text', 'spoiler', 'movie_id'])

is_starwars = reviews['movie_id'] == 2488496
starwars = reviews[is_starwars]

print(type(starwars))

## NEED THIS:
subj_verbs = list()
# not_stop_words = set(['i', 'you', 'he', 'she', 'it', 'we', 'they'])
# stop_words = [word for word in nlp.Defaults.stop_words if word not in not_stop_words]


for row, review in starwars.iterrows():
    
    
    ## NEED THIS
    pairs = list()
    doc = nlp(review.text)
    for k, sentence in enumerate(doc.sents):
        # print(k, sentence)
        for token in sentence:
            if (token.dep == nsubj or token.dep == nsubjpass) and token.head.pos == VERB:
            # and not token.lower_ in stop_words and not token.head.lemma_.lower() in stop_words:
                compounds = [child.lower_ for child in token.children if child.dep_ == 'compound']
                compounds.append(token.lower_)
                pairs.append('-'.join(compounds) + '|' + token.head.lemma_.lower())
        # print('---')
    subj_verbs.append(', '.join(pairs))
    
    
    
    
    if row % 100 == 0:
        print('Finished review ', row)
starwars.insert(loc=4, column='subj_verb', value=subj_verbs)

x = starwars['subj_verb'].tolist()
y = starwars['spoiler'].tolist()

## gotta save vec1
## text to one element list, vec1.
## abs value of probablity - 5 * 2

vec1 = CountVectorizer(tokenizer=lambda x: x.split(', '), min_df=10)
x = vec1.fit_transform(x)

svc = SVC(gamma=0.3)
svc.fit(x,y)
y_true = svc.predict(x)
print(f1_score(y, y_true))
with open('my_dumped_classifier.pkl', 'wb') as fid:
    cPickle.dump(svc, fid)
print("exported")