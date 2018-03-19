Who?
Aaron DePass (team leader), Chris Wolff, Jason Akers, Joungwon Kwon, Rob Arcand, and Zephyr Farah are the team members working on this project. The movie reviews we are working with are made by IMDb users (as opposed to reviews done exclusively by movie critics).

What?
We want to do a sentiment analysis of movie reviews on IMDb, especially on negatively- and positively-coded words, in order to see whether there is a correlation between the sentiment of reviews and the ratings they have, and how we can thoroughly analyze this potential connection. We have begun by looking through reviews on IMDb for the top 100 rated feature films that have been shown in English between 2007 and 2017. The top 100 were chosen because past that point, there are not many reviews for movies. We are also only looking at the 25 most helpful reviews, both because of the larger potential for trolls further down. This has given us 25,000 reviews to work with.

When?
We have chosen the top 100 rated feature films for each chosen year, from the years 2007 to 2017.

Where?
The movie reviews are written by IDMb users on the related IMDb webpage for the movie. There is a specific URL for the user reviews as well, from which we pulled the reviews.

Why?
Our team wants to know if we can condense movie reviews into a set of phrases or words that would still fairly accurateful represent the reviews' collective reflection of the movie. We want to explore how much one can take away from a set of movie reviews, made by different users, and still express the same core sentiments and ideas as the original reviews. In practice, this could be useful for those who do not want to read through the reviews, for any number of reasons (they have no time or energy for a variety of reasons, it is inefficient and therefore not worth it), but still want to have the same movie experience as those who may have more access to public opinions on movies.

How?
We first pulled the reviews from the IMDb website; the specific data we focused on are in the column headers of the raw data. Then, we wanted to make the data easier to read, so in cleaning the data, we assigned an ID number to each movie, so that the associated ID number with each review will tell which movie that review is about. Then, we focused on looking for errors in the data (i.e., Unicode mistakes), making a bag of words via tokenization, and examining word frequency.

Where from?
This data is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/
