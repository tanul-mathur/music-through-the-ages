# Music Through the Ages

A Data Geek's take on the question ***'How have music tastes changed through the years?'***


![](https://github.com/tanul-mathur/music-through-the-ages/blob/master/images/window_vinyl.jpg)
<span>Photo by <a href="https://unsplash.com/@shutters_guild?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Travis Yewell</a> on <a href="https://unsplash.com/@tanulmathur/likes?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>

This project is an attempt to collect relevant evidence (data) and analyzing it to get answers for these questions - 

* Are music trends actually shifting? 
* Are the same kind of songs popular that were chartbusters 50 years ago? 
* Or have we started to love radically different songs?  

&nbsp;

## Workflow
![](https://github.com/tanul-mathur/music-through-the-ages/blob/master/plots/Workflow.jpg)

## Story
[Link to the Medium article](https://tanulmathur.medium.com/music-through-the-ages-b7acbfa9eb7c)

## Key Highlight
> One underlying theme running across clusters and time is that we love energetic dance songs. The emotional gradient of songs may have shifted to a more neutral tone from the Happy notes of the yester years but throughout the 50 years we have always loved a song that makes us groove!  

&nbsp;

## Next Steps
There are few more interesting areas where I would like to expand this project -
1. Expanding coverage to include songs from (a) 1945, (b) other markets UK, India, etc.
2. Adding other dimensions of audio data like - genre, lyrics, major instruments used, etc.
3. It will be great to get sales information around individual albums to give depth into popularity beyond Billboard chart ranks
4. Web app to let users upload their favorite tracks and predict their age range
5. Web app that lets users create Spotify playlist of any year's Billboard Top 100 songs

## App
:notes: [![Music Through Ages](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tanul-mathur/music-through-the-ages/AppFinal.py)

Feel like playing around the dataset? Wonder which artist has the most Hits? Spoiler alert it's not Pink Floyd! Is The Weeknd on there? wait what-about The Beatles?? Head over to the Streamlit app and explore where your favorite artists are among the Top 100 and how their songs have evolved!

## Script Glossary
* [TopMusicChartsScraper.py](https://github.com/tanul-mathur/music-through-the-ages/blob/master/TopMusicChartsScraper.py) - Web scraping script to get track title, artist, rank from Billboard's Wikipedia pages
* [SpotifyGetAccessToken.py](https://github.com/tanul-mathur/music-through-the-ages/blob/master/SpotifyGetAccessToken.py) - Script to get Spotify API access token
* [GetSpotifyFeatures.py](https://github.com/tanul-mathur/music-through-the-ages/blob/master/GetSpotifyFeatures.py) - Script to extract Audio features from the Spotify API
* [AppFinal.py](https://github.com/tanul-mathur/music-through-the-ages/blob/master/AppFinal.py) - Main script for setting up the App
* [Helper.py](https://github.com/tanul-mathur/music-through-the-ages/blob/master/Helper.py) - Script containing functions needed for the App
