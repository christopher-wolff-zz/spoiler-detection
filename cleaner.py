"""Data cleaning for movie text data."""

__version__ = '0.1'
__date__ = '3/19/2018'


import json
# import nltk
# nltk.download()
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from helper import export_to_csv
from helper import export_to_json


def clean(reviews):
    """Clean the provided list of reviews.

    Mutates the list passed as a parameter.

    """
    for review in reviews:
        # get rid of commas in numeric values
        review['num_helpful_yes'] = review['num_helpful_yes'].replace(',', '')
        review['num_helpful_total'] = review['num_helpful_yes'].replace(',', '')
        # tokenize title and remove punctuation and stopwords
        stop_words = stopwords.words('english')
        title_tokens = word_tokenize(review['title'])
        title_words = [word.lower() for word in title_tokens if word.isalpha() and word not in stop_words]
        review['title_tokens'] = title_words
        # tokenize text and remove punctuation and stopwords
        text_tokens = word_tokenize(review['text'])
        text_words = [word.lower() for word in text_tokens if word.isalpha() and word not in stop_words]
        review['text_tokens'] = text_words
        # delete old keys
        del review['title']
        del review['text']


if __name__ == '__main__':
    with open('reviews_raw.json', 'r') as input_file:
        reviews = json.load(input_file)
    clean(reviews)
    export_to_csv(reviews)
    export_to_json(reviews)
