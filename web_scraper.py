"""A web scraper for IMDB."""


__version__ = '0.1'
__date__ = '3/19/2018'


import csv
import json
import requests

from bs4 import BeautifulSoup


base_url = 'http://www.imdb.com'


def scrape_movies(years, num_movies=100, debug=False) -> list:
    """Scrape the most popular movies from the specified years from IMDb.

    The method collects the unique identification number, name, year, average
    rating, total number of votes, and url for each movie. Only English movies
    that were categorized as feature films are considered.

    Args:
    =====
    years (list): The years to be considered
    num_movies (int): The maximum number of movies to be collected for each year
    debug (bool): Whether to display debug messages

    Returns:
    ========
    A list of dictionary objects representing the movies

    """
    movies = list()
    for year in years:
        if debug:
            print('Year: %d' % year)
        url = base_url + '/search/title'
        payload = {'year': year, 'languages': 'en', 'ref_': 'adv_prv',
                   'count': num_movies, 'sort': 'num_votes,desc',
                   'title_type': 'feature', 'view': 'advanced'}
        response = requests.get(url, params=payload)
        if debug:
            print('Movie URL: ' + response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for k, movie_div in enumerate(soup.find_all('div', class_='lister-item-content')):
            movie = dict()
            temp_1 = movie_div.h3.a['href']  # /title/tt...
            temp_2 = temp_1[9:]  # id starts at 9th character
            movie['id'] = temp_2[:temp_2.find('/')]
            movie['name'] = movie_div.h3.a.text
            movie['year'] = year
            movie['avg_rating'] = float(movie_div.strong.text)
            movie['num_votes'] = int(movie_div.find('span', attrs={'name': 'nv'})['data-value'])
            movie['url'] = base_url + temp_1
            movies.append(movie)
            if debug and (k + 1) % 10 == 0:
                print('Finished scraping %d movies' % (k + 1))
    return movies


def scrape_reviews(movies, debug=False) -> list:
    """Scrape the most helpful reviews for the given movies from IMDb.

    The method collects the 25 most helpful reviews for each movie, but discards
    those that do not have a rating. It collects the title, date, rating, full
    text, number of people that found the review helpful, total number of people
    who voted on the helpfulness of the review, url, and movie id of the movie
    that the review was for.

    Args:
    =====
    movies (list): The movies of interest
    debug (bool): Whether to display debug messages

    Returns:
    ========
    A list of review objects representing the reviews

    """
    reviews = list()
    for k, movie in enumerate(movies):
        if debug:
            print('Movie %d: ' % (k + 1), end='')
        question_mark_index = movie['url'].find('?')
        url = movie['url'][:question_mark_index] + 'reviews'
        payload = {'sort': 'helpfulnessScore', 'dir': 'desc'}
        response = requests.get(url, params=payload)
        if debug:
            print(response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for review_div in soup.find_all('div', class_='lister-item-content'):
            review = dict()
            rating = review_div.find('span', class_='rating-other-user-rating')
            if not rating:
                continue
            helpfulness = review_div.find('div', class_='actions text-muted').text
            tokens = helpfulness.strip().split()
            review['title'] = review_div.find('div', class_='title').text
            review['date'] = review_div.find('span', class_='review-date').text
            review['rating'] = int(rating.find('span').text)
            review['text'] = review_div.find('div', class_=["text show-more__control", "text show-more__control clickable"]).text
            review['num_helpful_yes'] = tokens[0]
            review['num_helpful_total'] = tokens[3]
            review['url'] = url
            review['movie_id'] = movie['id']
            reviews.append(review)
    return reviews


def export_to_csv(obj, file_name):
    """Export a list of dictionaries to a csv file.

    Args:
    =====
    obj (list): A list of dictionaries representing the object to be exported
    file_name (str): The destination file name

    """
    keys = obj[0].keys()
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(obj)


def export_to_json(obj, file_name):
    """Export a list of dictionaries to a json file.

    Args:
    =====
    obj (list): A list of dictionaries representing the object to be exported
    file_name (str): The destination file name

    """
    with open(file_name, 'w') as output_file:
        json.dump(obj, output_file)


if __name__ == '__main__':
    movies = scrape_movies(years=range(2008, 2018), num_movies=100, debug=True)
    reviews = scrape_reviews(movies, debug=True)
    print('Found %d movies and %d reviews' % (len(movies), len(reviews)))
    export_to_csv(movies, 'movies_raw.csv')
    export_to_csv(reviews, 'reviews_raw.csv')
    export_to_json(movies, 'movies_raw.json')
    export_to_json(reviews, 'reviews_raw.json')
