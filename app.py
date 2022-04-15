from http.client import HTTPResponse
import json
from flask import Flask, redirect, url_for, render_template, request
from spotify import *

app = Flask(__name__, static_folder="./static")

user_data = {
    'username': 'User',
    'playlists': [],
    'rand_playlists': [],
    'playlist': 'No Playlist',
    'tracks': [],
    'index': 0
}

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if 'username' in request.form:
            username = request.form['username']
            user_data['username'] = username

            # first, get user's playlists
            playlists=get_users_playlists(username)
            user_data['playlists'] = playlists

            # next, get random playlists from spotify
            rand_playlists=get_random_playlists()
            user_data['rand_playlists'] = rand_playlists

            user_data['index'] = 0
        if 'submit_shuffle' in request.form:
            print('shuffle clicked')
        if 'submit_p_shuffle' in request.form:
            print('psuedo clicked')
        if 'submit_f_t_b' in request.form:
            print('f t b clicked')
        if 'submit_b_t_f' in request.form:
            print('b t f clicked')
        if 'select_playlist' in request.form:
            user_data['playlist'] = request.form['select_playlist']
            user_data['tracks'] = get_tracks_array(user_data['username'], user_data['playlist']) 
            user_data['index'] = 0
        if 'select_random_playlist' in request.form:
            user_data['playlist'] = request.form['select_random_playlist']
            user_data['tracks'] = get_random_tracks_array(user_data['playlist'])
            user_data['index'] = 0
        if 'forward_button' in request.form:
            user_data['index'] += 1    
        if 'back_button' in request.form:
            user_data['index'] -= 1   
        if 'done' in request.form:
            user_data['index'] += 1
        
        # return the username to display it
        # call function from spotify to get their available playlists

    return render_template("index.html", username=user_data['username'], playlists=user_data['playlists'], rand_playlists=user_data['rand_playlists'], playlist=user_data['playlist'], tracks=user_data['tracks'], index=user_data['index'])


if __name__ == '__main__':
    app.run(debug=True)
