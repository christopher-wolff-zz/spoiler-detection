import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
text =""
sent_tokenize(text)
word_tokenize(text)

# Import the pandas package, then use the "read_csv" function to read
# the labeled training data
import pandas as pd       
train = pd.read_csv("labeledTrainData.tsv", header=0, \
                    delimiter="\t", quoting=3)
                    
                    train.shape
(25000, 3)

>>> train.columns.values
array([id, sentiment, review], dtype=object)

# Import BeautifulSoup into your workspace
from bs4 import BeautifulSoup             

# Initialize the BeautifulSoup object on a single movie review     
example1 = BeautifulSoup(train["review"][0])  

# Print the raw review and then the output of get_text(), for 
# comparison
print train["review"][0]
print example1.get_text()

import re
# Use regular expressions to do a find-and-replace
letters_only = re.sub("[^a-zA-Z]",           # The pattern to search for
                      " ",                   # The pattern to replace it with
                      example1.get_text() )  # The text to search
print letters_only

lower_case = letters_only.lower()        # Convert to lower case
words = lower_case.split()               # Split into words
print train["review"][0]