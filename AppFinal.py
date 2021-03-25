import numpy as np
from PIL import Image
import streamlit as st
from Helper import load_data, summary_poster

stats_df = load_data("./data/df_wclusters.csv")
color_map_df = load_data("./data/color_map_df.csv")

st.set_page_config(page_title="Music Through the Ages", 
                   page_icon=":notes:", 
                   layout='wide')

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------
title_image = Image.open("./plots/AppTitle.jpg")
st.image(title_image)

st.markdown("A Data Geek's take on the question ***'How have music tastes changed through the years?'***")
st.markdown("This app is meant as a playground to explore the dataset used in the" +
            " [Music through the Ages](https://github.com/tanul-mathur/music-through-the-ages)\
                project. It contains 50 years of \
                    [Billboard's Top 100 Year-End Hot singles]\
                        (https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2020) \
                            clustered by the themes identified in the project.")
#---------------------------------------------------------------#
# SELECT ARTIST AND SETUP DATA
#---------------------------------------------------------------#
sorted_artists = stats_df.groupby('search_artist')['search_query'].count()\
    .sort_values(ascending=False).index

st.markdown("### **Select Artist:**")
select_artist = []

select_artist.append(st.selectbox('', sorted_artists))

#Filter df based on selection
artist_df = stats_df[stats_df['search_artist'].isin(select_artist)]

major_cluster = artist_df.groupby('clusters')['search_query'].count()\
    .sort_values(ascending = False).index[0]

#Setting up color palette dict
color_dict = dict(zip(color_map_df['clusters'], color_map_df['colors']))

col1, col2 = st.beta_columns(2)
    
with col1:
    st.markdown(f"**Total Songs:** {artist_df.shape[0]}")
    st.markdown(f"**Top Song:** " +\
                f"{artist_df.loc[artist_df['track_rank']==np.min(artist_df['track_rank']),'search_query'].values[0]}")
    
with col2:
    st.markdown(f"**Highest Rank:** {np.min(artist_df['track_rank'])}")
    st.markdown(f"**Major Cluster:** {major_cluster}")

st.text("")
#---------------------------------------------------------------#
# CREATE SUMMARY POSTER
#---------------------------------------------------------------#
fig = summary_poster(artist_df, color_dict)
st.write(fig)

#---------------------------------------------------------------#
# PROJECT BRIEF
#---------------------------------------------------------------#
workflow_image = Image.open("./plots/Workflow.jpg")

st.text("")
st.markdown("### Project Brief  ([Medium Article](https://tanulmathur.medium.com/music-through-the-ages-b7acbfa9eb7c))")
st.image(workflow_image)

with st.beta_expander("Spotify Audio Feature definitions"):
    
    col1, col2, col3 = st.beta_columns(3)
    
    with col1:
        st.subheader("Acousticness")
        st.markdown("A confidence measure from 0.0 to 1.0 of whether the "+
                    "track is acoustic. 1.0 represents high confidence the track is acoustic.")
        
        st.subheader("Liveness")
        st.markdown("Detects the presence of an audience in the recording. Higher liveness values "+
                    "represent an increased probability that the track was performed live. A value above 0.8 "+
                    "provides strong likelihood that the track is live.")
        
        st.subheader("Speechiness ")        
        st.markdown("Detects the presence of spoken words in a track. The more exclusively speech-like the "+
            "recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values "+
            "above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and"+
            "0.66 describe tracks that may contain both music and speech, either in sections or layered, including such"+
            "cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks") 
        
    with col2:
        st.subheader("Danceability")
        st.markdown("Describes how suitable a track is for dancing based on a "+
                    "combination of musical elements including tempo, rhythm stability, beat strength, "+
                    "and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")
        
        st.subheader("Instrumentalness")
        st.markdown("Predicts whether a track contains no vocals. "+
            "“Ooh” and “aah” sounds are treated as instrumental in this context. "+
            "Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness "+
            "value is to 1.0, the greater likelihood the track contains no vocal content. Values "+
            "above 0.5 are intended to represent instrumental tracks, but confidence is higher as the "+
            "value approaches 1.0")
        
        st.subheader("Tempo")
        st.markdown("The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is"+
            "the speed or pace of a given piece and derives directly from the average beat duration.")

    with col3:
        st.subheader("Energy")
        st.markdown("Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity "+
                    "and activity. Typically, energetic tracks feel fast, loud, and noisy."+
                    "For example, death metal has high energy, while a Bach prelude scores low on the scale. "+
                    "Perceptual features contributing to this attribute include dynamic range, perceived loudness, "+
                    "timbre, onset rate, and general entropy.")
        
        st.subheader("Loudness")
        st.markdown("The overall loudness of a track in decibels (dB). Loudness values are "+
                    "averaged across the entire track and are useful for comparing relative loudness "+
                    "of tracks. Loudness is the quality of a sound that is the primary psychological "+
                    "correlate of physical strength (amplitude). Values typical range between -60 and 0 db")
        
        st.subheader("Valence")
        st.markdown("A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. "+
            "Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low"+
            "valence sound more negative (e.g. sad, depressed, angry).")
        
