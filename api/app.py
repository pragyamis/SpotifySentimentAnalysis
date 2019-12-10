
# coding: utf-8

# In[4]:

from flask import Flask
from flask import request, jsonify
from flask import Flask, redirect, request, session, url_for, jsonify
import json
from json import dumps
from utilities import spotifydata
from utilities import geniuslyrics
import spotipy.util as util
#import sentiment_analysis

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'supersecret'

token = util.prompt_for_user_token(
        username="psamrai7",
        scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing",
        client_id="06fbc86c86fb476fa9154ebbcea09a2a",
        client_secret="1ad66a32c99944ffa9728e38629c5ebb",
        redirect_uri="http://localhost/")   

def get_songs(data):    
    for p in data['history'][0]['songs']:
            print('id: ' + p['id'])
            print('name: ' + p['name'])
            print('sentiment: ' + p['sentiment'])        
            print('')
        
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Songs Sentiment Archive</h1>
<p>A prototype API for Songs Sentiment Analysis</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/songs', methods=['GET'])
def api_all():
    #if 'token' in request.args:
    #    token = int(request.args['token'])
    user_songlisten_data = spotify_current_user_recently_played(token)
    lyrics_data = geniuslyrics(user_songlisten_data)
    #sentiment_data = #sentanalysis call(lyrics_data)  # should be in format of dictionary
    # temp-------------------------------------------
    filename = '..\SongAnalysisSample.json'
    with open(filename) as json_file:
        sentiment_data = json.load(json_file)
    #--------------------------------------------------
    #output file
    with open('sentimentdata.txt', 'w') as outfile:
        json.dump(sentiment_data, outfile)
    return jsonify(sentiment_data['history'][0]['songs'])
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)


