library(cleanNLP)
library(FSelectorRcpp)
library(tidytext)
library(tidyverse)
library(tm)

reviews <- read_csv("data/reviews_temp.csv")
movies <- read_csv("data/movies_raw.csv")

reviews <- reviews %>%
  left_join(movies, by = c("movie_id" = "id")) %>%
  select(review_id, text, spoiler, year, name, movie_id) %>%
  unnest_tokens("word", "text", token = "words")

reviews %>%
  group_by(name) %>%
  count() %>%
  arrange(desc(n)) %>%
  head(10)

# The Dark Knight: 0468569
# Star Wars: Episode VIII - The Last Jedi: 2527336
# The Lord of the Rings: The Fellowship of the Ring: 0120737
# Star Wars: The Force Awakens: 2488496

rev <- reviews %>%
  filter(movie_id == "2527336") %>%
  select(review_id, spoiler) %>%
  mutate(review_id = as.character(review_id))

r <- reviews %>%
  filter(movie_id == "2527336")
r <- r %>%
  anti_join(get_stopwords("en")) %>%
  group_by(review_id) %>%
  count(word)
mft <- r %>%
  group_by(word) %>%
  count() %>%
  filter(nn >= 100) %>%
  select(word) %>%
  pull(word)
r <- r %>%
  filter(word %in% mft)
dtm <- r %>%
  cast_dtm(term = "word", document = "review_id", value = "n") %>%
  as.matrix()
dtm <- dtm %>%
  data.frame() %>%
  rownames_to_column(var = "review_id") %>%
  left_join(rev, by = "review_id") %>%
  mutate(
    spoiler = spoiler.x,
    is_spoiler = spoiler.y
  ) %>%
  select(-one_of("spoiler.x", "spoiler.y"))
ig <- information_gain(is_spoiler ~ . - review_id, dtm, type = "infogain")
ig %>%
  arrange(desc(importance)) %>%
  head(15)

rev <- reviews %>%
  select(review_id, spoiler) %>%
  mutate(review_id = as.character(review_id))
revs <- reviews %>%
  select(review_id, text, spoiler) %>%
  unnest_tokens("word", "text", token = "words")
revs %>%
  tm_map(stemDocument, language = "english")
revs <- revs %>%
  anti_join(get_stopwords("en")) %>%
  group_by(review_id) %>%
  count(word)
mft <- revs %>%
  group_by(word) %>%
  count() %>%
  filter(nn >= 100) %>%
  select(word) %>%
  pull(word)
revs <- revs %>%
  filter(word %in% mft)
dtm <- revs %>%
  cast_dtm(term = "word", document = "review_id", value = "n") %>%
  as.matrix() %>%
  data.frame() %>%
  rownames_to_column(var = "review_id") %>%
  left_join(rev, by = "review_id") %>%
  mutate(
    spoiler = spoiler.x,
    is_spoiler = spoiler.y
  ) %>%
  select(-one_of("spoiler.x", "spoiler.y"))
ig <- information_gain(is_spoiler ~ . - review_id, dtm, type = "infogain")
