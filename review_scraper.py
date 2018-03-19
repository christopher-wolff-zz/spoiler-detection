import requests
from bs4 import BeautifulSoup

years = range(2008, 2018)
movies_per_year = 100

base_url = 'http://www.imdb.com'


def scrape_movies():
    """..."""
    movies = list()
    for year in years:
        print('Year: %d' % year)
        movie_url = base_url + '/search/title'
        movie_params = {'year': year, 'sort': 'num_votes,desc', 'ref_': 'adv_prv',
                        'count': movies_per_year, 'view': 'advanced',
                        'languages': 'en', 'title_type': 'feature'}
        movie_response = requests.get(movie_url, params=movie_params)
        print('Movie URL: ' + movie_response.url)
        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
        for k, movie_div in enumerate(movie_soup.find_all('div', class_='lister-item-content')):
            movie = dict()
            movie['name'] = movie_div.h3.a.text
            movie['year'] = year
            movie['rating'] = float(movie_div.strong.text)
            movie['votes'] = movie_div.find('span', attrs={'name': 'nv'})['data-value']
            movie['url'] = movie_div.h3.a['href']
            movies.append(movie)
            if (k + 1) % 10 == 0:
                print('Finished scraping %d movies' % (k + 1))
    return movies


def scrape_reviews(movies):
    """..."""
    for k, movie in enumerate(movies):
        print('Movie %d: ' % (k + 1), end='')
        question_mark_index = movie['url'].find('?')
        review_url = base_url + movie['url'][:question_mark_index] + 'reviews'
        review_params = {'sort': 'helpfulnessScore', 'dir': 'desc'}
        review_response = requests.get(review_url, params=review_params)
        print(review_response.url)
        review_soup = BeautifulSoup(review_response.text, 'html.parser')
        reviews = list()
        for review_div in review_soup.find_all('div', class_='lister-item-content'):
            review = dict()
            rating = review_div.find('span', class_='rating-other-user-rating')
            if rating is None:
                continue
            review['rating'] = int(rating.find('span').text)
            review['title'] = review_div.find('div', class_='title').text
            review['date'] = review_div.find('span', class_='review-date').text
            review['text'] = review_div.find('div', class_=["text show-more__control", "text show-more__control clickable"])
            reviews.append(review)
        movie.update({'reviews': reviews})


if __name__ == '__main__':
    movies = scrape_movies()
    scrape_reviews(movies)
    n = 0
    for movie in movies:
        print(len(movie['reviews']))
        n += len(movie['reviews'])
    print(n)
