import math
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
                   'languages': 'en', 'title_type': 'feature'}
        response = requests.get(url, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_divs = soup.find_all('div', class_='lister-item-content')
        for movie_div in movie_divs:
            movie = {}
            movie['name'] = movie_div.h3.a.text
            movie['year'] = year
            movie['rating'] = float(movie_div.strong.text)
            movie['votes'] = movie_div.find('span', attrs={'name': 'nv'})['data-value']
            movies.append(movie)

for movie in movies:
    print(movie)
