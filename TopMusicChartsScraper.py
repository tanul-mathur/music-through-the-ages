
#Load libraries
import os
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from IPython.display import clear_output


#Function definitions to handle fetch tasks
def fetch_artist(td,x):    
    if td[x].a:
        return td[x].a.string
    else:
        return td[x].string

def fetch_title(td,x):
    if td[x].a:
        return td[x].a['title']
    else:
        return td[x].string

#Function for getting track details from row
def fetch_track_details(row):
    """Parse single row from webpage and extract track details

    Args:
        row (string): Single row from webpage

    Returns:
        list: List of track details - rank, title, artist
    """    
    
    td = row.find_all('td')
    
    #handling edge case - 2020
    if len(td)==3:
        track_rank = td[0].string
        track_artist = fetch_artist(td,2)        
        track_title = fetch_title(td,1)
    
    #handle edge case - 2012
    elif len(td)==4:
        track_rank = re.sub(r'[\.\n]', '', td[0].string)
        track_artist = fetch_artist(td,3)        
        track_title = fetch_title(td,1)

    else:
        track_rank = row.find_all('th')[0].string.replace('\n','')
        track_artist = fetch_artist(td,1)
        track_title = fetch_title(td,0)

    return [track_rank, track_title, track_artist]

# Function to get dataframe from wikipedia link
def get_df_tracks(year_no, target_url):
    """Parse given webpage and extract track details for a given year

    Args:
        year_no (int): Target year to get track details
        target_url (string): Web link of the target url to scrape details from

    Returns:
        Pandas DataFrame: Combined dataframe for all the tracks from the specified year,\
              consisting of track details - rank, title, artist
    """
    
    html_string = requests.get(target_url + f"{year_no}")
    parsed_html = BeautifulSoup(html_string.text, 'html.parser')
    parsed_table = parsed_html.find_all('table','wikitable')

    rows = [row for row in parsed_table[0].find_all('tr')]

    bucket_track_df = pd.DataFrame(data = list(pd.Series(rows[1:]).map(fetch_track_details)), 
                                    columns = ['track_rank', 'track_title', 'track_artist'])
    
    bucket_track_df['year'] = year_no

    return bucket_track_df

#Get and combine track details for multiple years
def get_and_combine_track_details(target_url, min_year, max_year):
    """Get combined dataframe of track details from given wikipedia link \
        for the specified year-range. (Currently built for \
            Billboard-Year-End-Hot-100-Singles and for years 1970 to 2020)

    Args:
        target_url (string): Web link of the target url to scrape details from
        min_year (int): Start year
        max_year (int): End year (excluded, minimum range: 2 years)

    Returns:
        Pandas DataFrame: Combined dataframe for all the tracks in the specified year\
             range, consisting of track details : rank, title, artist
    """

    loop_range = max_year - min_year - 1
    
    for year in range(min_year, max_year):
        
        clear_output(wait = True)
        os.system('cls')
        
        if year == min_year:
            collector_df = get_df_tracks(year,target_url)
        else:
            collector_df = collector_df.append(get_df_tracks(year,target_url), 
                                               ignore_index = True) 

        #Print progress bar and %
        iter = year - min_year        
        percent_complete = int(round(iter*100/loop_range,0))        
        print(f"{percent_complete} % complete!"
                + '\n' + '='*percent_complete + '>'
                + f"\n Latest year fetched: {year}")

        time.sleep(1)


    return collector_df
