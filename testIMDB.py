from requests import get
from bs4 import BeautifulSoup
url = 'http://www.imdb.com/title/tt1856010/reviews?start='

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)
movie_containers = html_soup.find_all('div', class_ = 'text')
print(type(movie_containers))
print(len(movie_containers))

first_movie = movie_containers[0]
print(first_movie)
