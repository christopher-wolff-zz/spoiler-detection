import requests
import math
from bs4 import BeautifulSoup

years = range(2017, 2018)
movies_per_year = 100

base_url = 'http://www.imdb.com'

movies = list()
for year in years:
    print('Year %d' % year)
    movie_url = base_url + '/search/title'
    movie_params = {'year': year, 'sort': 'num_votes,desc', 'ref_': 'adv_prv',
                    'count': movies_per_year, 'view': 'advanced',
                    'languages': 'en', 'title_type': 'feature'}
    movie_response = requests.get(movie_url, params=movie_params)
    movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
    movie_divs = movie_soup.find_all('div', class_='lister-item-content')
    for movie_div in movie_divs:
        movie = dict()
        movie['name'] = movie_div.h3.a.text
        movie['year'] = year
        movie['rating'] = float(movie_div.strong.text)
        movie['votes'] = movie_div.find('span', attrs={'name': 'nv'})['data-value']
        movie['url'] = movie_div.h3.a['href']
        movies.append(movie)

for movie in movies:
    question_mark_index = movie['url'].find('?')
    review_url = base_url + movie['url'][:question_mark_index] + 'reviews'
    review_params = {'sort': 'helpfulnessScore', 'dir': 'desc'}
    review_response = requests.get(review_url, params=review_params)
    review_soup = BeautifulSoup(review_response.text, 'html.parser')
    review_divs = movie_soup.find_all('div', class_ = )
    print(review_soup)
