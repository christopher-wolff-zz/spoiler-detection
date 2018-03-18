import requests
from bs4 import BeautifulSoup

years = range(2008, 2018)
num_movies = 100

movies = []
for year in years:
    print('Year %d' % year)
    url = 'http://www.imdb.com/search/title'
    payload = {'year': year, 'sort': 'num_votes,desc', 'count': num_movies,
               'view': 'advanced', 'ref_': 'adv_prv', 'languages': 'en',
               'title_type': 'feature'}
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
