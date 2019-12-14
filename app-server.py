
# coding: utf-8

# In[4]:

from flask import Flask
from flask import request, jsonify
from flask import Flask, redirect, request, session, url_for, jsonify
from flask_cors import CORS
import json
from json import dumps
from api.utilities import spotifydata
from api.utilities import geniuslyrics
import spotipy.util as util
import sentiment_prediction as sa
from datetime import date, datetime
import pandas as pd
from fcache.cache import FileCache

#import sentiment_analysis

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})
app.config["DEBUG"] = False
app.config['SECRET_KEY'] = 'supersecret'
sent_p = sa.SentAnalysisPrediction()
gen_cache = FileCache('genius_cache', flag="cs")
sentiment_cache = FileCache('sentiment_cache', flag="cs")

def get_usertoken():
    token = util.prompt_for_user_token(
            username="psamrai7",
            scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing",
            client_id="de3fbad698124c53a722cd1283fb2e0d",
            client_secret="5edc515babd54bd1959b3a5624cf548e",
            redirect_uri="http://3.15.223.174:4200/main")

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Songs Sentiment Archive</h1>
<p>A prototype API for Songs Sentiment Analysis</p>'''

def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))
        
# A route to return all of the available entries in our catalog.
@app.route('/songs', methods=['GET'])
def api_all():
    token = request.args.get('access_token')
    user_songlisten_data = spotifydata.spotify_current_user_recently_played(token)
    user_songlisten_data['play_timestamp'] = pd.to_datetime(user_songlisten_data['play_times'])
    user_songlisten_data['history_timestamp'] = user_songlisten_data['play_timestamp'].apply(lambda x: x.date())
    song_data = user_songlisten_data[["song_names","primary_artist"]]
    song_data.drop_duplicates()
    songlisten_data = user_songlisten_data[['play_timestamp','song_names','history_timestamp']]
    songlisten_data.columns = ['Play Timestamp','Song Title','Timestamp']
    date_list = set(user_songlisten_data['history_timestamp'])
    song_list = []
    lyrics_data = geniuslyrics.geniuslyricspull(song_data, gen_cache)

    sentiment_data = pd.DataFrame()
    for row in lyrics_data.itertuples():
        sentiment  = sent_p.predict_sentiment_with_cache(row.Song_Title, row.Lyrics, sentiment_cache)
        sent_row = {
            'Song Title' : row.Song_Title,
            'Sentiment' : sentiment,
            'Lyrics' : row.Lyrics
        }
        sentiment_data = sentiment_data.append(sent_row, ignore_index=True)

    lyricshistory_data = pd.merge(songlisten_data, sentiment_data, on ='Song Title')
    history = []
    for d in date_list:    
        history_dict = {}
        df1 = lyricshistory_data[(lyricshistory_data['Timestamp'] == d)]
        df1.columns = ['timestamp','song','histtimestamp','sentiment', 'lyrics']
        df1 = df1.drop('histtimestamp',axis = 1)
        history_dict['timestamp'] = d
        history_dict['songs'] = df1.to_dict('records')
        history.append(history_dict)
    result = {"user":"","history":history}
    app_json = json.dumps(result, default=json_serial)
    return app_json

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4201)



