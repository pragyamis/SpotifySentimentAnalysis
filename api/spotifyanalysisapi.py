
# coding: utf-8

# In[4]:

from flask import Flask
from flask import request, jsonify
from json import dumps

app = Flask(__name__)
app.config["DEBUG"] = True


import json
filename = '..\SongAnalysisSample.json'
with open(filename) as json_file:
    data = json.load(json_file)

def get_songs():    
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
@app.route('/songs/all', methods=['GET'])
def api_all():
    return jsonify(data['history'][0]['songs'])

@app.route('/songs', methods=['GET'])
def song_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No name field provided. Please specify an song name."
    results = []
    for song in data['history'][0]['songs']:
        if song['id'] == id:
            results.append(song)
    return jsonify(results)
    
#if __name__ == '__main__':
app.run()


