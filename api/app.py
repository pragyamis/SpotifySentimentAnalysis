
# coding: utf-8

# In[4]:
from flask import Flask
from flask import request, jsonify
from flask import Flask, render_template, redirect, request, session, make_response
import json
from json import dumps
from utilities import spotifydata
from utilities import geniuslyrics
import spotipy
import spotipy.util as util
import pandas as pd
import sys
sys.path.insert(0,'..')
import sentiment_prediction as sp
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/songs', methods=['GET'])
def query_strings():
    token = request.args['access_token']
    song_titles =   spotify_current_user_recently_played(token)
    #song_titles = pd.read_csv('.//utilities//user1_songlisten_data.csv')
    all_song_data = geniuslyrics.geniuslyricspull(song_titles.head(2))
    all_song_data['Sentiment'] = all_song_data.Lyrics.apply(lambda x: sp.predict_sentiment(x))
    #output file
    with open('song_sentiments.json', 'w') as outfile:
        json.dump(all_song_data[['Song Title','Sentiment']].to_json(orient ='records'), outfile)
    return jsonify(all_song_data[['Song Title','Sentiment']])
    
if __name__ == '__main__':
    app.run(debug=True)


