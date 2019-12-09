import spotipy
import spotipy.util as util
import json
import types
import pandas as pd
import json
from pandas.io.json import json_normalize

#auth with spotipy and spotify app auth info here
#see documentation for spotipy/spotify setup: 
#https://spotipy.readthedocs.io/en/latest/?highlight=current_user_recently_played

def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played', limit=limit)

def spotify_current_user_recently_played(token):
    spotify = spotipy.Spotify(auth=token)

    spotify.current_user_recently_played = types.MethodType(current_user_recently_played, spotify)
    recent_listening = spotify.current_user_recently_played(limit=50)

    play_times, song_names, song_uri ,song_popularity ,song_duration , song_explicit ,  number_artists , primary_artist=[]
    second_artist,third_artist,fourth_artist,fifth_artist = []

    for i in range(len(recent_listening['items'])):
        play_times.append(recent_listening['items'][i]['played_at']) #play time (when track was played)
        song_names.append(recent_listening['items'][i]['track']['name']) #get each song name
        song_uri.append(recent_listening['items'][i]['track']['uri']) #get each song uri (unique record id for spotify)
        song_popularity.append(recent_listening['items'][i]['track']['popularity'])#get song popularity rank
        song_duration.append(recent_listening['items'][i]['track']['duration_ms']) #get duration time in ms
        song_explicit.append(recent_listening['items'][i]['track']['explicit']) #get explicit content bool 

        #each primary artist involved in song
        primary_artist.append(recent_listening['items'][i]['track']['artists'][0]['name'])
        #second, third, fourth, or fifth artist involved (if exist)

        n_artists = len(recent_listening['items'][i]['track']['artists'])
        number_artists.append(n_artists)

        if n_artists>1: 
            second_artist.append(recent_listening['items'][i]['track']['artists'][1]['name']) #get second artist
        else: 
            second_artist.append("")
        if n_artists>2: 
            third_artist.append(recent_listening['items'][i]['track']['artists'][2]['name']) #get third artist
        else: 
            third_artist.append("")    
        if n_artists>3: 
            fourth_artist.append(recent_listening['items'][i]['track']['artists'][3]['name']) #get fourth artist
        else: 
            fourth_artist.append("")    
        if n_artists>4: 
            fifth_artist.append(recent_listening['items'][i]['track']['artists'][4]['name']) #get fifth artist
        else: 
            fifth_artist.append("")

    user_songlisten_data = pd.DataFrame(
    {"play_times" : play_times,  
    "song_names" : song_names,  
    "song_uri" : song_uri,  
    "song_popularity" : song_popularity,  
    "song_duration" : song_duration,  
    "song_explicit" : song_explicit,  
    "number_artists" : number_artists,
    "primary_artist" : primary_artist,  
    "second_artist" : second_artist,  
    "third_artist" : third_artist,  
    "fourth_artist" : fourth_artist,  
    "fifth_artist" : fifth_artist
    })
    user_songlisten_data
    print(type(user_songlisten_data))

    #output file
    user_songlisten_data.to_csv("user1_songlisten_data.csv", encoding='utf-8', index=False)
    return user_songlisten_data
