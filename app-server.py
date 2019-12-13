
# coding: utf-8

# In[4]:

from flask import Flask
from flask import request, jsonify
from flask import Flask, redirect, request, session, url_for, jsonify
from flask_cors import CORS
import jsons
from json import dumps
from api.utilities import spotifydata
from api.utilities import geniuslyrics
import spotipy.util as util
import sentiment_prediction as sa

#import sentiment_analysis

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})
app.config["DEBUG"] = False
app.config['SECRET_KEY'] = 'supersecret'
sent_p = sa.SentAnalysisPrediction()

def get_usertoken():
    token = util.prompt_for_user_token(
            username="psamrai7",
            scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing",
            client_id="de3fbad698124c53a722cd1283fb2e0d",
            client_secret="5edc515babd54bd1959b3a5624cf548e",
            redirect_uri="http://3.15.223.174:4200/main")

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

class response_object:
    username = ''
    history = []

class history:
    timestamp = None
    songs = []

class song_data:
    name = ''
    sentiment = ''
    lyrics = ''

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

# A route to return all of the available entries in our catalog.
@app.route('/songs', methods=['GET'])
def api_all():
    #if 'token' in request.args:
    #    token = int(request.args['token'])
    token = request.args.get('access_token')
    user_songlisten_data = spotifydata.spotify_current_user_recently_played(token)

    song_list = []

    for song in user_songlisten_data:
        print(song)


    lyrics_data = geniuslyrics.geniuslyricspull(user_songlisten_data)
    lyrics_data['Lyrics'] = lyrics_data['Lyrics'].str.replace('\[[A-Za-z0-9: ]+\] ','')

    for index, song in lyrics_data.iterrows():
        songObject = song_data()
        songObject.name = song["Song Title"]
        songObject.lyrics = song["Lyrics"]
        songObject.sentiment = sent_p.predict_sentiment(songObject.lyrics)
        song_list.append(songObject)

    res : response_object = response_object()
    res.username = ''

    hist = history()
    hist.songs = song_list
    hist.timestamp = "12-01-2019"

    hist2 = history()
    hist2.songs = song_list
    hist2.timestamp = "12-02-2019"

    hist3 = history()
    hist3.songs = song_list
    hist3.timestamp = "12-03-2019"

    res.history.append(hist)
    res.history.append(hist2)
    res.history.append(hist3)
    #app_json = json.dumps(res)
    app_json = jsons.dumps(res)

    return app_json

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4201)


