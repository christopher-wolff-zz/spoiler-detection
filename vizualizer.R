library(tidyverse)
library(scales)

# load data
reviews <- read_csv("data/reviews_cleanV3.csv")
movies <- read_csv("data/movies_rawV3.csv")

# plot 1
ggplot(reviews, aes(x = rating)) +
  geom_histogram(bins = 10) +
  theme_bw()

gg <- ggplot(data = reviews, mapping = aes(x = rating)) +
  geom_histogram(
    bins = 10,
    color = "black",
    fill = "white"
  ) +
  labs(title = "Rating distribution across reviews",
       x = "Rating",
       y = "Count"
  ) +
  theme_minimal() +
  scale_x_continuous(breaks = 1:10) +
  scale_y_continuous(label = comma)

png("plots/ratings_histogram.png")
print(gg)
dev.off()

# plot 2
revs <- movies %>%
  select(id, date) %>%
  left_join(reviews, ., by = c("movie_id" = "id"))
revs <- revs %>%
  mutate(date_diff = difftime(date.x, date.y, units = "days"))

ggplot(revs, aes(x = date_diff, y = spoiler)) +
  geom_point()

filter(revs, date_diff < 0) %>%
  group_by(movie_id) %>%
  count() %>%
  arrange(desc(n)) %>%
  View()
max(revs$date_diff)
