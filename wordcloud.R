## Making a word cloud with English text ##

rm(list=ls())   # Clearing memory
install.packages("tm")  # for text mining
install.packages("SnowballC") # for text stemming
install.packages("wordcloud") # word-cloud generator 
install.packages("RColorBrewer") # color palettes 
install.packages("tidyverse")
install.packages("scales")

library(tm)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)
library(scales)

# Read the text file
setwd("/Users/jkwon/Desktop/")
text <- read.csv("top1000.csv", header=T)
head(text, 10)

#Bar plot of Top 100
png("top50barplot.png", width=12,height=8, units='in', res=300)
par(mar = rep(0, 4))
barplot(text[1:50,]$count, las=2, names.arg=text[1:50,]$word,
        col="white",cex.names=1)
title(main="Top 50 words", adj=0, line=1, cex=16)
mtext("Count", side=2, line=3, cex=1.5)
mtext("Word", side=1, line=3.5, cex=1.5)


# Word Cloud Black and White
set.seed(1234)
wordcloud(words = text$word, freq = text$count, 
          min.freq = 100, max.words=100, 
          scale=c(3, 0.5), random.order=FALSE, 
          rot.per= 0.15, colors="#000000")
# Word Cloud no rotation with Blue
set.seed(1234)
wordcloud(words = text$word, freq = text$count, max.words=100, 
          scale=c(6, 1), random.order=FALSE, 
          rot.per= 0, colors=brewer.pal(3,"Blues"))
# Word Cloud no rotaiton with Black and save
png("wordcloud_packages.png", width=12,height=8, units='in', res=300)
par(mar = rep(0, 4))
wordcloud(words = text$word, freq = text$count, max.words=100, 
          scale=c(6, 1), random.order=FALSE, 
          rot.per= 0, colors="#000000")

