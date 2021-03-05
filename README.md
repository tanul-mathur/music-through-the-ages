---
title: 'Music Through the Ages'
author: 'Tanul Mathur'
date: 'March 4th, 2021'
---

# Music Through the Ages

A Data Geek's take on the question ***'How has music changed through the years?'*** Or is there a change at all? Do we still like the same kind of songs as we did 50 years ago? Or have we started to love radically different songs?  

Exploring shifting trends in the music industry using Top 100 songs from the Billboard Year-end Hot singles charts as a guide. Analyzed over 5,000 songs over 50 years from 1970 to 2020 using audio features from the Spotify API.

![<span>Photo by <a href="https://unsplash.com/@shutters_guild?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Travis Yewell</a> on <a href="https://unsplash.com/@tanulmathur/likes?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>](/images/window_vinyl.jpg)


## Data Extraction
Used 'BeautifulSoup' library to scrape the list of songs from the Wikipedia pages of *Billboard's Year End Top 100 Hot singles charts* from the US market. Then extracted Audio Features from the Spotify API for all of these tracks. Ended up creating a wrapper script to extract this data for any year range. **Link to my repo here.**

### Spotify Audio Features
Quick context around some of the Spotify Audio feature definitions for the ones most relevant to this analysis : *Complete list can be found [here](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-features)*

* Acousticness - A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
* Danceability - Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
* Energy - Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
* Valence - A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

Although these features don't represent any conventional genres but they are still pretty useful representations of audio features. 

## Data description

A quick and dirty boxplot of the *scaled* dataset to see some overall characterstics of the Top 100 songs.

![](/plots/initial_data_boxplot.jpg)

 * Dance, Energy, Loudness are skewed towards the higher side
 * Similarly on the other end of the spectrum highly speechy and acoustic songs are a rarity among the top 100
 * Valence - Emotional spectrum of the songs seems to be quite wide spread across happiness to sadness
 * and finally, some features worth dropping from further analysis as they show little to no variation across the data - Key, Mode, Instrumentalness, Liveness, Duration, Track Popularity

 ## Clustering

### Intuition - the What and Why?
Clustering is a popular technique to group together data into hopefully meaningful clusters that can further help us analyse the trends.  

### Toe-Dip
Now even after having a strong intuition to to perform Clustering it is important to understand if the dataset actually has the potential of showing any clusters. This can be done by calculating a 'Hopkins Score' on the scaled dataset. Essentially, this score checks if the dataset is derived from a uniform distribution. If the resulting value is closer to 0 it would suggest that the data is not uniformly distributed and there is merit in using clustering techniques to classify the observations. [Reference](https://pyclustertend.readthedocs.io/en/master/)

For this Top 100 songs dataset the Hopkins Score came out as ***~0.176***, indicating there were clusters waiting to be uncovered!

### Elbow test to find the optimal number of clusters
Now that we have made up our mind to look under the hood for clusters. Let's see what should be the ideal number of clusters.
Below is a chart representing the results of a classic 'Elbow test'. This consists of the number of clusters on x-axis and their respective SSD on the y-axis. The idea being that as the number of clusters increases the SSD will tend to approach 0 and the 'elbow' on the line chart will indicate the point from which the reduction in SSD is very less compared to the increase in no. of clusters. Making the point the most optimum number of clusters for the given dataset.

![](https://github.com/tanul-mathur/music-through-the-ages/blob/master/plots/elbow_plot.html)



