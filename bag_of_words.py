"""Tools for creating a bag of words from a cleaned list of reviews.

The output for our dataset, sorted in descending order of term frequency and
only displaying the top 20 rows, is:

rank term  frequency
1    movie      63280
2    film       51570
3    one        29273
4    like       26828
5    story      19087
6    good       18377
7    would      17940
8    really     16689
9    even       16102
10   see        15690
11   time       15504
12   much       14012
13   character  13035
14   well       12913
15   could      12733
16   characters 12664
17   get        12628
18   first      12438
19   people     12034
20   great      11945

"""


import csv
import json
from nltk.corpus import stopwords


def create_bow(reviews, debug=False) -> dict:
    """Create a bag of words.

    Filters out stop words. Each key represents a word that appears in the
    review and the corresponding value represents the number of times that word
    appears in all reviews.

    """
    bag_of_words = dict()
    stop_words = stopwords.words('english')
    for k, review in enumerate(reviews):
        words = review['text'].split(' ')
        for word in words:
            if word in stop_words:
                continue
            if word not in bag_of_words:
                bag_of_words[word] = 0
            bag_of_words[word] += 1
        if debug and (k + 1) % 100 == 0:
            print('Finished processing %d reviews' % (k + 1))
    return bag_of_words


if __name__ == '__main__':
    with open('reviews_clean.json', 'r') as input_file:
        reviews = json.load(input_file)
    bag_of_words = create_bow(reviews, debug=True)
    # export to csv
    keys = bag_of_words.keys()
    with open('bag_of_words.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerow(bag_of_words)
    # export to json
    with open('bag_of_words.json', 'w') as output_file:
        json.dump(bag_of_words, output_file)
