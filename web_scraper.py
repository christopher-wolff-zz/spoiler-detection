import csv
import json
import requests

from bs4 import BeautifulSoup


base_url = 'http://www.imdb.com'


def scrape_movies(num_movies, year_start, year_end) -> list:
    """..."""
    movies = list()
    for year in range(year_start, year_end + 1):
        print('Year: %d' % year)
        movie_url = base_url + '/search/title'
        movie_params = {'year': year, 'sort': 'num_votes,desc', 'ref_': 'adv_prv',
                        'count': num_movies, 'view': 'advanced',
                        'languages': 'en', 'title_type': 'feature'}
        movie_response = requests.get(movie_url, params=movie_params)
        print('Movie URL: ' + movie_response.url)
        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
        for k, movie_div in enumerate(movie_soup.find_all('div', class_='lister-item-content')):
            movie = dict()
            url_temp_1 = movie_div.h3.a['href']  # /title/tt...
            url_temp_2 = url_temp_1[9:]  # id starts at 9th character
            movie['id'] = url_temp_2[:url_temp_2.find('/')]
            movie['name'] = movie_div.h3.a.text
            movie['year'] = year
            movie['rating'] = float(movie_div.strong.text)
            movie['votes'] = int(movie_div.find('span', attrs={'name': 'nv'})['data-value'])
            movie['url'] = base_url + url_temp_1
            movies.append(movie)
            if (k + 1) % 10 == 0:
                print('Finished scraping %d movies' % (k + 1))
    return movies


def scrape_reviews(movies) -> list:
    """..."""
    reviews = list()
    for k, movie in enumerate(movies):
        print('Movie %d: ' % (k + 1), end='')
        question_mark_index = movie['url'].find('?')
        review_url = movie['url'][:question_mark_index] + 'reviews'
        review_params = {'sort': 'helpfulnessScore', 'dir': 'desc'}
        review_response = requests.get(review_url, params=review_params)
        print(review_response.url)
        review_soup = BeautifulSoup(review_response.text, 'html.parser')
        for review_div in review_soup.find_all('div', class_='lister-item-content'):
            review = dict()
            rating = review_div.find('span', class_='rating-other-user-rating')
            if not rating:
                continue
            review['title'] = review_div.find('div', class_='title').text
            review['date'] = review_div.find('span', class_='review-date').text
            review['rating'] = int(rating.find('span').text)
            review['text'] = review_div.find('div', class_=["text show-more__control", "text show-more__control clickable"]).text
            review['url'] = review_url
            review['movie_id'] = movie['id']
            reviews.append(review)
    return reviews


def export_to_csv(obj, file_name):
    """Export a list of dictionaries to a csv file."""
    keys = obj[0].keys()
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(obj)


def export_to_json(obj, file_name):
    """Export a list of dictionaries to a json file."""
    with open(file_name, 'w') as output_file:
        json.dump(obj, output_file)


if __name__ == '__main__':
    movies = scrape_movies(100, 2008, 2017)
    reviews = scrape_reviews(movies)
    print('Found %d movies and %d reviews' % (len(movies), len(reviews)))
    export_to_csv(movies, 'movies_raw.csv')
    export_to_csv(reviews, 'reviews_raw.csv')
    export_to_json(movies, 'movies_raw.json')
    export_to_json(reviews, 'reviews_raw.json')
