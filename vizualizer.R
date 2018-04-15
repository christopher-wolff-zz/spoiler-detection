library(tidyverse)
library(scales)

reviews <- read_csv('data/reviews_cleanV3.csv')

ggplot(reviews, aes(x = rating)) +
  geom_histogram(bins = 10) +
  theme_bw()

ggplot(data = reviews, mapping = aes(x = rating)) +
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
