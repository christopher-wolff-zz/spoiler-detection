library(tidyverse)
library(scales)
library(ngram)

# load data
reviews <- read_csv("data/reviews_clean_nonstop.csv")
movies <- read_csv("data/movies_raw.csv")

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
reviews <- reviews %>%
  rowwise() %>%
  mutate(word_count = wordcount(text)) %>%
  ungroup()

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

# table 2
revs <- filter(reviews, word_count >= 2)
ngs <- list()
for (k in 0:80) {
  ngs[k+1] <- ngram(reviews$text[(k*10000+1):((k+1)*10000+1)], n = 1) %>%
    get.phrasetable() %>%
    as.tibble() %>%
    head(1000)
  print(paste0("Finished ", k))
}


for (k in 0:80) {
  
}
