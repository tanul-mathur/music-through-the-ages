#Load Libraries
import os
import re
import pandas as pd
import time
import requests
from SpotifyGetAccessToken import get_access_token
from TopMusicChartsScraper import get_and_combine_track_details
from IPython.display import clear_output


# Class defining spotify objects
class spotify_track(object):
    '''Class to fetch track info from spotify based on title, artist.\
        Also keeps everything neat and tidy'''

    def __init__(self,headers, track_title, artist_name, pick=0,
                 search_limit=5,search_market = 'US', 
                 search_type = 'track'):
        '''Initializes and gets track info from spotify's search API'''

        self.headers = headers
        self.pick = pick
        self.search_limit = search_limit
        self.search_market = search_market
        self.search_type = search_type
        
        # base URL of all Spotify API endpoints
        self.base_url = 'https://api.spotify.com/v1/'

        #cleaning extra content inside brackets present in wiki track titles
        clean_track_title = re.sub(r'\ \([\w \d]*\)','', track_title)
        self.search_query = re.sub(' ','%20',clean_track_title)
        self.search_artist = re.sub(' ','%20',artist_name)
        

    def check_token(self):
        """Check token validity and refresh if required

        Returns:
            dict: Checked and validated spotify access token
        """                
        
        global headers
        #Handling token expiry
        try:
            r = requests.get(f"{self.base_url}search/",
                                f"q={self.search_query}%20artist:{self.search_artist}&type={self.search_type}"+
                                f"&limit={self.search_limit}&market={self.search_market}",
                                headers=self.headers)             
            r.json()['error']

            print('Refreshing Token.')
            
            headers = get_access_token()
            self.headers = headers
            time.sleep(1)
            return headers

        except:
            try:
                #Handling the edge case JSONDecodeError from the AudioFeatures API result
                # Track ID from the URI
                track_id = re.sub('spotify:track:','',r.json()['tracks']['items'][self.pick]['uri'])
                
                r2 = requests.get(f"{self.base_url}audio-features/{track_id}",
                                            headers=self.headers)
                r2 = r2.json()
                
                #If no error continue with same
                print('Checked Token, refresh not required')
                time.sleep(0.5)
                return self.headers
            
            except:
                #If error refresh token
                print('Refreshing Token.')                
                headers = get_access_token()
                self.headers = headers
                time.sleep(1)
                return headers
            

    def get_track_details(self):
        """Get meta data for given track from Spotify API as dict.

        Returns:
            dict: Details returned - artist, artist_uri, album, album_uri,\
                track, track_uri, track_popularity, duration_ms        
        """     

        # actual GET request to the Search API
        r = requests.get(f"{self.base_url}search/",
                        f"q={self.search_query}%20artist:{self.search_artist}&type={self.search_type}"+
                        f"&limit={self.search_limit}&market={self.search_market}",
                        headers=self.check_token())
        
        r = r.json()        
        
        try:
            #Fetch Track details from response json and store in dict
            track_details_dict = {
                'search_query' : re.sub('%20', ' ',self.search_query),
                'search_artist' : re.sub('%20', ' ',self.search_artist),
                'artist' : r['tracks']['items'][self.pick]['artists'][0]['name'],
                'artist_uri' : r['tracks']['items'][self.pick]['artists'][0]['uri'],
                'album' : r['tracks']['items'][self.pick]['album']['name'],
                'album_uri' : r['tracks']['items'][self.pick]['album']['uri'],
                'track' : r['tracks']['items'][self.pick]['name'],
                'track_uri' : r['tracks']['items'][self.pick]['uri'],
                'track_popularity' : r['tracks']['items'][self.pick]['popularity'],
                'duration_ms' : r['tracks']['items'][self.pick]['duration_ms']
            }
        except:            
            #if no search entry return NAs
            track_details_dict = {
                'search_query' : re.sub('%20', ' ',self.search_query),
                'search_artist' : re.sub('%20', ' ',self.search_artist),
                'artist' : 'NA',
                'artist_uri' : 'NA',
                'album' : 'NA',
                'album_uri' : 'NA',
                'track' : 'NA',
                'track_uri' : 'NA',
                'track_popularity' : 'NA',
                'duration_ms' : 'NA'
            }
        
        #add track uri
        self.track_uri = track_details_dict['track_uri']
        
        return track_details_dict

    def get_audio_features(self):
        """Fetches Meta data and Audio features from spotify using track uri

        Returns:
            dict: Consisting of both meta data and audio features
        """        
        
        #Fetch Meta Data            
        track_details_dict = self.get_track_details()

        #In case track is not available in Spotify search return NAs
        if self.track_uri == 'NA':
            features_req = {
                'danceability': 'NA',
                'energy': 'NA',
                'key': 'NA',
                'loudness': 'NA',
                'mode': 'NA',
                'speechiness': 'NA',
                'acousticness': 'NA',
                'instrumentalness': 'NA',
                'liveness': 'NA',
                'valence': 'NA',
                'tempo': 'NA',
                'type': 'NA',
                'id': 'NA',
                'uri': 'NA',
                'track_href': 'NA',
                'analysis_url': 'NA',
                'duration_ms': 'NA',
                'time_signature': 'NA'
            }
        else:
            try:
                # Track ID from the URI
                track_id = re.sub('spotify:track:','',self.track_uri)

                # actual GET request to Spotify Audio Features API
                features_req = requests.get(f"{self.base_url}audio-features/{track_id}",
                                            headers=self.check_token())

                features_req = features_req.json()
                
            except:
                # In case token expired refresh token
                #print(features_req)
                time.sleep(5)
                self.headers = get_access_token()
                
                # Track ID from the URI
                track_id = re.sub('spotify:track:','',self.track_uri)

                # actual GET request to Spotify Audio Features API
                features_req = requests.get(f"{self.base_url}audio-features/{track_id}",
                                            headers=self.check_token())

                features_req = features_req.json()

        #Add audio feature details to the dict
        track_details_dict.update(features_req.items())

        return track_details_dict


#Final wrapper function to get both tracks and audio features
def scrape_tracks_get_features(min_year, max_year):
    """Wrapper function to scrape tracks for given year range and get their\
        audio features from Spotify. (Currently built for \
            Billboard-Year-End-Hot-100-Singles and for years 1970 to 2020). \
                Performance benchmark : Takes 10-15 minutes to get df of\
                    200 songs.

    Args:
        min_year (int): Starting year
        max_year (int): End year (excluded, minimum range: 2 years)

    Returns:
        Pandas DataFrame: Combined dataframe with track rank, title, artist & \
            spotify audio features
    """    
    
    # Get tracks from scraper
    print("Getting tracks from the web...")

    #Default url for Billboard Year End Hot 100 singles
    target_url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_'
    #min_year = 1970; #max_year = 2021
    
    #Function call to scrape track details from wiki url
    all_tracks_df = get_and_combine_track_details(target_url, min_year, max_year)

    print(f"Fetched {all_tracks_df.shape[0]} tracks from {min_year} to {max_year}.")

    print("Now getting audio features for these tracks from Spotify!")

    #Get initial access token
    headers = get_access_token()

    #Token initial search to get sample dict keys
    t = spotify_track(headers, 'War','Edwin Starr',0).get_audio_features()

    #MAIN LOOP TO RUN ALONG THE TRACK LIST DF AND FETCH AUDIO FEATURES INTO DATAFRAME
    iter = 0
    collect_list = []
    collect_key = list(t.keys())
    start_time = time.time()

    for track, artist, year in \
        all_tracks_df.loc[:,['track_title','track_artist', 'year']].itertuples(index = False):
        
        collect_dict = spotify_track(headers, track, artist, 0).get_audio_features()
        collect_list.append(list(collect_dict.values()))        

        os.system('cls')
        clear_output(wait=True)
        na_rows = sum([x[2]=='NA' for x in collect_list])#/25

        print(f"{year}, {track} by {artist}, {iter} - No. of NA rows {na_rows}")
        iter += 1
        time.sleep(0.5)

    collect_df = pd.DataFrame(collect_list, columns = collect_key)

    #post time taken
    current_time = time.time()
    minutes_elapsed = divmod(current_time - start_time,60)[0]
    print(f"Time taken to get: {round(minutes_elapsed/60,2)} hour(s)")

    #combine with the track list df from wiki scraper (all_tracks_df)
    comb_df = pd.merge(all_tracks_df, collect_df, how = 'left', left_index = True, right_index = True)
    
    #Write to file
    #comb_df.to_csv('data/combined_track_audio_detials.csv')
    
    return comb_df