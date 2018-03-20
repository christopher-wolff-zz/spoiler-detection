## Making a word cloud with English text ##

rm(list=ls())   # Clearing memory

install.packages("tm")  # for text mining
install.packages("SnowballC") # for text stemming
install.packages("wordcloud") # word-cloud generator 
install.packages("RColorBrewer") # color palettes 

library(tm)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)

# Read the text file
setwd("/Users/jkwon/Desktop/movie-review-summarizer-master")
text <- read.csv("reviews.csv",header=T)
reviews <- text[[4]]
docs<-Corpus(VectorSource(reviews))

inspect(docs)
# Convert the text to lower case
docs <- tm_map(docs, content_transformer(tolower))

# Remove punctuations
docs <- tm_map(docs, removePunctuation)
inspect(docs)

# Remove english common stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))
# Text stemming
docs <- tm_map(docs, stemDocument)
dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

findFreqTerms(dtm, lowfreq = 2)           # frequent terms

barplot(d[1:20,]$freq, las = 2, names.arg = d[1:20,]$word,
        col ="lightblue", main ="Most frequent words",
        ylab = "Word frequencies")

set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 3,
          max.words=150, scale=c(2,0.5), random.order=FALSE, rot.per= 0.15, 
          colors=brewer.pal(8, "Dark2"))

