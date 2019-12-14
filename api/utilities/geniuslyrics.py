import pandas as pd
import numpy as np
import requests
import lyricsgenius as lg
import re

def geniuslyricspull(song_titles):
    genius = lg.Genius("eOwlhC7-N4Lr7bq9YUD8J-khhwTxKwi0svZVzwlN2Io8shw4RW9pLcaUU6yLMK_K")

    #song_titles = pd.read_csv("user1_songlisten_data.csv")
    song_titles.fillna('').replace('', np.nan)

    #print(song_titles['song_names'][0])

    #in general additional artists are included in the some name 
    #(example: THRU THE NIGHT (feat. Bryson Tiller)" by Jack Harlow)
    # song_titles = song_titles.assign(Artist= song_titles.primary_artist.fillna('') + ' ' +  
    #                                  song_titles.second_artist.fillna('') + ' ' +  
    #                    song_titles.third_artist.fillna('') + ' ' +  song_titles.fourth_artist.fillna('') + 
    #                                  ' ' +  song_titles.fifth_artist.fillna('') )
    song_titles = song_titles.assign(Artist = song_titles.primary_artist)
    song_titles.rename(
        columns = {'song_names':'song_title'}, 
        inplace = True)

    #print(song_titles.columns)
    #print(song_titles)

    all_song_data = pd.DataFrame()

    for i in range(0, len(song_titles)):
        #rolling_pct = int((i/len(song_titles))*100)
        #print(str(rolling_pct) + "% complete." + " Collecting Record " + str(i) +" of " +
        #      str(len(song_titles)) +". Year " + str(song_titles.iloc[i]['Year']) + "." + " Currently collecting " + 
        #      song_titles.iloc[i]['Song Title'] + " by " + song_titles.iloc[i]['Artist'] + " "*50, end="\r")
        song_title = song_titles['song_title'][i]
        song_title = re.sub(" and ", " & ", song_title)
        artist_name = song_titles['Artist'][i]
        artist_name = re.sub(" and ", " & ", artist_name)

        try:
            song = genius.search_song(song_title, artist=artist_name)
            song_album = song.album
            song_lyrics = re.sub("\n", " ", song.lyrics) #Remove newline breaks, we won't need them.
            song_lyrics = song_lyrics.replace('\[[A-Za-z0-9: ]+\] ','')
            song_url = song.url
            song_artist = song.artist
            song_year = song.year
        except Exception as e:
            print("Exception at pulling data from genius {0}".format(e))
            song_album = "null"
            song_lyrics = "null"
            song_url = "null"
            song_artist = "null"
            song_year = "null"

        row = {
            "Song Title": song_titles['song_title'][i],
            "Artist": song_titles['Artist'][i],
            "Song Artist": song_artist,
            "Lyrics": song_lyrics,
            "Song URL": song_url,
            "Release Date": song_year
        }
        all_song_data = all_song_data.append(row, ignore_index=True)
        #print(all_song_data)
        #all_song_data.to_csv("user1_songlyrics_data.csv")
    return all_song_data
