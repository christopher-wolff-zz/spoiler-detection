"""A web scraper for IMDB.

1. We used the BeautifulSoup python package for web scrap data
to scrape the most popular movies (top 100) from the specified years from the IMDb.
The method collects the unique identification number, name, year, average rating,
total number of votes, and URL for each movie. Only English movies that were categorized
as feature films are considered. The arguments that are used here are years (list)
which are the years to be considered, num_movies (int) which are the maximum number
of movies to be collected for each year, and debug (bool) which displays debug messages.

2. We scrapped the most helpful reviews for the given movies from IMDb.
The method collects the 25 most helpful reviews for each movie, but discards those that
do not have a rating. It collects the title, date, rating, full text, number of people that found
the review helpful, total number of people who voted on the helpfulness of the review, URL, and the movie id.
The arguments that are used are movies (list) which are the movies of interest and debug (bool)
which are whether to display debug messages. It returns a list of dictionary objects representing the movies.

3. We exported a list of dictionaries to a csv file to save. The arguments that obj (list)
is a list of dictionaries representing the object to be exported and file_name (str)
is the destination file name. We exported a list of dictionaries to a json file, too.
The arguments are obj (list) which is a list of dictionaries representing the object
to be exported and file_name (str) which is the destination file name.

"""


__version__ = '0.1'
__date__ = '3/19/2018'


import requests
from bs4 import BeautifulSoup
import json

from helper import export_to_csv
from helper import export_to_json


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
            ## print(movie['id'])
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
        url2 = movie['url'][:question_mark_index] + 'reviews/_ajax?ref_=undefined&paginationKey='
        payload = {'sort': 'helpfulnessScore', 'dir': 'desc'}
        response = requests.get(url, params=payload)
        if debug:
            ## print(response.url)
            print("URL2" + url2)
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = requests.get(url2)
        broth = BeautifulSoup(main_content.text, 'lxml')
        while(broth.findAll('div', class_ = 'load-more-data')):
              for review_div in broth.find_all('div', class_='lister-item-content'):
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
              containers = broth.findAll('div', class_ = 'load-more-data')
              data = containers[0]['data-key']
              urlkey = url2 + data
              print(urlkey)
              main_content = requests.get(urlkey)
              broth = BeautifulSoup(main_content.text, 'lxml')
    return reviews


if __name__ == '__main__':
    x = 2003
    y = 2004
    while(y <= 2018):
        mname = 'movies_raw' + str(x) + '.csv'
        rname = 'reviews_raw' + str(y) + '.csv'
        movies = scrape_movies(years=range(x, y), num_movies=100, debug=True)
        reviews = scrape_reviews(movies, debug=True)
        print('Found %d movies and %d reviews' % (len(movies), len(reviews)))
        with open('movies_raw2.json', "a") as data:
            data.write(json.dumps(movies))
            data.close()
        with open('reviews_raw2.json', "a") as data:
            data.write(json.dumps(reviews))
            data.close()
        ##with open('movies_raw2.csv', "a") as data:
            ##data.write(movies)
           ## data.close()
        ##with open('reviews_raw2.csv', "a") as data:
            ##data.write(reviews)
            ##data.close()
        export_to_csv(movies, mname)
        export_to_csv(reviews, rname)
        ## export_to_json(movies, 'movies_raw2.json')
        ## export_to_json(reviews, 'reviews_raw2.json')
        x = x + 1
        y = y + 1
