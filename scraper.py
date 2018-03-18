import math
from pprint import pprint
import requests
from bs4 import BeautifulSoup

num_titles = 254417  # in 2017
titles_per_page = 50
num_pages = math.ceil(num_titles / titles_per_page)

for k in range(10):
    print(f'Page {k + 1}')
    url = 'http://www.imdb.com/search/title'
    payload = {'release_date': 2017, 'sort': 'user_rating,desc', 'view': 'advanced',
               'page': k + 1, 'ref_': 'adv_prv'}
    response = requests.get(url, params=payload)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    pprint(html_soup)
