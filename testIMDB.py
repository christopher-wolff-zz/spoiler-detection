from requests import get
import requests
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

# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
pages = range(1, 10)
years = [2015, 2016, 2017]

for year in years:
	for page in pages:
		url = 'http://www.imdb.com/search/title'
		payload = {'year': year, 'sort':'num_votes,desc', 'view': 'advanced',
		'page':page, 'ref_': 'adv_prv', 'languages': 'en'
		}
		response2 = requests.get(url, params = payload)
		html_soup = BeautifulSoup(response2.text, 'html.parser')
		type(html_soup)
		movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
		for container in movie_containers:
			if container.find('div', class_ = 'ratings-metascore') is not None:
				name = container.h3.a.text
        		names.append(name)
        		print(name)
        		# The year
        		year = container.h3.find('span', class_ = 'lister-item-year').text
        		years.append(year)
        		print(year)
        	# The IMDB rating
        		imdb = float(container.strong.text)
        		imdb_ratings.append(imdb)
        		print(imdb)
        		# The Metascore
        		# The number of votes
        		vote = container.find('span', attrs = {'name':'nv'})['data-value']
       	 		votes.append(int(vote))
        		print(vote)


