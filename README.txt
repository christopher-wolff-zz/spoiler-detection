Who?
Aaron DePass (team leader), Christopher Wolff, Jason Akers, Joungwon Kwon, Rob Arcand, and Zephyr Farah are the team members working on this project. The movie reviews we are working with are made by IMDb users (as opposed to reviews done exclusively by movie critics).

What?
We want to do a sentiment analysis of movie reviews on IMDb, especially on negatively- and positively-coded words, in order to see whether there is a correlation between the sentiment of reviews and the ratings they have, and how we can thoroughly analyze this potential connection. We have begun by looking through reviews on IMDb for the top 100 rated feature films that have been shown in English between 2008 and 2017. The top 100 were chosen because past that point, there are not many reviews for movies. We are also only looking at the 25 most helpful reviews, both because of the larger potential for trolls further down. This has given us 23,000 reviews to work with.

Where?
We have chosen the top 100 rated feature films for each chosen year, from the years 2008 to 2017.

Where?
The movie reviews are written by IDMb users on the related IMDb webpage for the movie. There is a specific URL for the user reviews as well, from which we pulled the reviews.

Why?
Our overall goal is to condense movie reviews into a set of phrases or words that are still fairly accurate and represent the reviews' collective reflection or sentiment of the movie. We want to explore how much one can take away from a set of movie reviews, made by different users, and still express the same core sentiments and ideas as the original reviews. In practice, this could be useful for those who do not want to read through the reviews, for any number of reasons (they have no time or energy, it is inefficient, not worth it), but still want to have adequate knowledge about public opinion of a movie before watching it. 

How?
We first pulled the reviews from the IMDb website; the specific data we focused on are in the column headers of the raw data. Then, we wanted to make the data easier to read, so in cleaning the data, we assigned an ID number to each movie, so that the associated ID number with each review will tell which movie that review is about. IMDb sorts reviews by helpfulness, which we thought would offer us a relatively even distribution of positive and negative reviews. We chose to look at user reviews, mainly because it was semantically easier to access them via site URL. Since we thought lower-rated movies would be more likely to have less reviews, we figured we would try to assess what a “balanced” distribution would be once we web scrape all of the movies on the above list. Then, we focused on looking for errors in the data (i.e., Unicode mistakes), making a bag of words via tokenization, and examining word frequency (this one we did through R).

With about 12,000 movies released in between 2017 and 2008, we decided to limit our data to 1,000 films total (100 films per year) to make it easier to parse a large number of reviews for each film in a reasonable amount of time.  We also limited our data set to a maximum of 25 reviews per film, discarding reviews that don’t have a rating. We determined how the URL and HTML was organized for each page, then using a for loop, scraped text from the corresponding div tag within each HTML file. We also filtered out any foreign language films and reviews to limit our language analysis to English.

Although an argument may be that we would get only positive reviews — this is not true. We are collecting data from the top 100 most rated movies, not the top 100 movies. Furthermore, we are collecting data from the top 25 most helpful reviews. This means that users voted “yes, this review was helpful” or “no, this review wasn’t helpful”. This means that regardless if the review was positive or negative people could still rate it helpful or not. 


Licensing:
We plan to release this data under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/
