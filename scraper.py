import math
from pprint import pprint
import requests
from bs4 import BeautifulSoup

years = range(2008, 2018)
movies_per_year = 100
movies_per_page = 50
num_pages = math.ceil(movies_per_year / movies_per_page)

movies = []
for year in years:
    for page in range(1, num_pages + 1):
        print('Year %d, Page %d' % (year, page))
        url = 'http://www.imdb.com/search/title'
        payload = {'year': year, 'sort': 'num_votes,desc',
                   'view': 'advanced', 'page': page, 'ref_': 'adv_prv',
                   'languages': 'en'}
        response = requests.get(url, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
