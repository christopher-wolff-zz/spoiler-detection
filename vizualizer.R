library(tidyverse)
library(scales)
library(ngram)
library(rjson)

# load data
reviews <- read_csv("data/reviews_clean_nonstop.csv")
movies_raw <- read_csv("data/movies_raw.csv")
movies <- fromJSON(file = "data/movies_clean.json")

# count words
reviews <- reviews %>%
  rowwise() %>%
  mutate(word_count = wordcount(text)) %>%
  ungroup()

# plot 1
ggplot(reviews, aes(x = rating)) +
  geom_histogram(bins = 10) +
  theme_bw()

ggplot(data = reviews, mapping = aes(x = rating)) +
  geom_bar(
    color = "black",
    fill = "white"
  ) +
  labs(title = "Rating distribution across reviews",
       x = "Rating",
       y = "Count"
  ) +
  theme_minimal() +
  scale_x_continuous(breaks = 1:10) +
  scale_y_continuous(label = comma) +
  theme(
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    title = element_text(size = 16)
  )

# plot 2
revs <- movies %>%
  select(id, date) %>%
  left_join(reviews, ., by = c("movie_id" = "id"))
revs <- revs %>%
  mutate(date_diff = as.numeric(difftime(date.x, date.y, units = "days")))

ggplot(revs, aes(x = date_diff, y = spoiler)) +
  geom_point(alpha = 0.01, size = 1) +
  geom_smooth(method = "gam")

# plot 3
ggplot(data = revs, mapping = aes(x = date_diff)) +
  geom_histogram(
    bins = 200,
    color = "black",
    fill = "white"
  ) +
  labs(
    title = "Differences between review dates and movie US release dates",
    x = "Time difference (days)",
    y = "Count"
  ) +
  scale_x_continuous(limits = c(-100, 500)) +
  scale_y_continuous(label = comma) +
  theme_minimal() +
  theme(
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    title = element_text(size = 16)
  )

# plot 4
reviews %>%
  mutate(spoiler = case_when(
    spoiler == 0 ~ "no",
    spoiler == 1 ~ "yes"
  )) %>%
ggplot(aes(x = word_count)) +
  geom_density(aes(fill = factor(spoiler)), alpha = 0.7) +
  theme_bw() +
  labs(
    title = "Review word count distribution",
    subtitle = "for spoilers vs. non-spoilers",
    x = "Number of words",
    y = "Density"
  ) +
  scale_x_continuous(limit = c(0, 1000)) +
  scale_fill_discrete(name = "Spoiler") +
  theme(
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    title = element_text(size = 16),
    legend.text = element_text(size = 16)
  )

# plot 5
reviews %>%
  ggplot(aes(x = word_count, y = num_helpful_yes)) +
  geom_smooth(method = "lm") +
  theme_bw() +
  theme(
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    title = element_text(size = 16)
  ) +
  labs(
    title = "Number of 'helpful' votes vs. review length",
    subtitle = "estimated by a linear regression model",
    x = "Number of words",
    y = "Number of 'helpful' votes"
  )

# plot 6
ngram(text, n = 2)

# table 1
reviews %>%
  group_by(spoiler) %>%
  count()

ng <- paste(reviews$text[1:2], collapse = ' , ') %>%
  ngram(n = 2)
get.phrasetable(ng)

# table 3 - ngrams
revs <- filter(reviews, word_count >= 4)
ngs <- ngram(reviews$text[1:10000], n = 1) %>%
  get.phrasetable() %>%
  as.tibble() %>%
  head(10000)
for (k in 1:80) {
  ngs <- ngram(reviews$text[(k*10000+1):((k+1)*10000)], n = 1) %>%
    get.phrasetable() %>%
    as.tibble() %>%
    head(10000) %>%
    rbind(ngs, .)
  print(paste0("Finished ", k))
}

results <- ngs %>%
  group_by(ngrams) %>%
  summarize(n = sum(freq)) %>%
  arrange(desc(n))
results <- results %>%
  mutate(prop = n / sum(n)) %>%
  head(1000) %>%
  mutate(ngrams = str_trim(ngrams))
results <- select(results, ngrams, n)

write.csv(results, "data/top1000.csv", row.names = F)

# movie analysis
genres <- vector()
for (movie in movies) {
  for (genre in movie$genres) {
    genres <- append(genres, genre)
  }
}
genres <- unique(genres)

# plot 7
wanted_genres <- c("Romance", "Action", "Horror", "Fantasy")

ratings_romance <- vector()
names_romance <- vector()
ids_romance <- vector()

ratings_action <- vector()
names_action <- vector()
ids_action <- vector()

ratings_horror <- vector()
names_horror <- vector()
ids_horror <- vector()

ratings_fantasy <- vector()
names_fantasy <- vector()
ids_fantasy <- vector()

for (movie in movies) {
  for (genre in movie$genres) {
    if (genre == "Romance") {
      ratings_romance <- append(ratings_romance, movie$avg_rating)
      names_romance <- append(names_romance, movie$name)
      ids_romance <- append(ids_romance, movie$id)
    }
    if (genre == "Action") {
      ratings_action <- append(ratings_action, movie$avg_rating)
      names_action <- append(names_action, movie$name)
      ids_action <- append(ids_action, movie$id)
    }
    if (genre == "Horror") {
      ratings_horror <- append(ratings_horror, movie$avg_rating)
      names_horror <- append(names_horror, movie$name)
      ids_horror <- append(ids_horror, movie$id)
    }
    if (genre == "Fantasy") {
      ratings_fantasy <- append(ratings_fantasy, movie$avg_rating)
      names_fantasy <- append(names_fantasy, movie$name)
      ids_fantasy <- append(ids_fantasy, movie$id)
    }
  }
}

r1 <- tibble(
  rating = ratings_romance,
  name = names_romance,
  id = ids_romance,
  genre = "Romance"
)
r2 <- tibble(
  rating = ratings_action,
  name = names_action,
  id = ids_action,
  genre = "Action"
)
r3 <- tibble(
  rating = ratings_horror,
  name = names_horror,
  id = ids_horror,
  genre = "Horror"
)
r4 <- tibble(
  rating = ratings_fantasy,
  name = names_fantasy,
  id = ids_fantasy,
  genre = "Fantasy"
)

ratings <- rbind(r1, r2, r3, r4)
ratings <- mutate(ratings, rating = as.numeric(rating))

ggplot(ratings, aes(x = genre, y = rating)) +
  geom_violin(draw_quantiles = c(.25, .50, .75)) +
  theme_bw() +
  labs(
    title = "Movie rating comparison for different genres",
    x = "Genre",
    y = "Rating"
  ) +
  theme(
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    title = element_text(size = 16),
    legend.text = element_text(size = 16)
  )

ratings %>%
  filter(genre == "Action") %>%
  arrange(desc(rating)) %>%
  head(5)
ratings %>%
  filter(genre == "Fantasy") %>%
  arrange(desc(rating)) %>%
  head(5)
ratings %>%
  filter(genre == "Horror") %>%
  arrange(desc(rating)) %>%
  head(5)
ratings %>%
  filter(genre == "Romance") %>%
  arrange(desc(rating)) %>%
  head(5)
