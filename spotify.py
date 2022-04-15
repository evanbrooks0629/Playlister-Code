import requests
import base64

# TODO

# [x] reload new token on an interval
# [x] pop up window for random playlist
# [x] random playlist to show 10 playlists with 50-100 tracks

# [ ] doubly linked list for forward / backward playback
# [ ] create LL based off original order of playlist
# [ ] to play forward, go from head->next until next is None
# [ ] to play backward, go from tail->next until next is None

# REFRESH TOKEN #

def get_new_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {}
    data = {}

    # converts client id and client secret to base64
    message = f"{client_id}:{client_secret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    data['grant_type'] = 'client_credentials'
    headers['Authorization'] = f"Basic {base64Message}"

    # send post, extract token
    response = requests.post(url=url, headers=headers, data=data)
    token = response.json()['access_token']

    return token

# generate token each time the page is opened to avoid oauth issues
client_id = "0b34a65d9de54a1b8b2280ecaa02a6be"
client_secret = "dd9bcf36376648168b60955899678d39"
token = get_new_token(client_id, client_secret)

##### SELECT PLAYLIST FUNCTIONS #####

def get_playlist_tracks(user_id, playlist_id):
    response = requests.get(
        f"https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "limit": '500',
            "offset": '0'
        }
    )

    json_response = response.json()

    return json_response

def get_rand_playlist_tracks(playlist_id):
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "limit": '500',
            "offset": '0'
        }
    )

    json_response = response.json()

    return json_response
     

def get_users_playlists(user_id):
    # Get the playlists of the user
    # Return array of playlists
    response = requests.get(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    json_response = response.json()


    #return json_response of playlist objects array
    if json_response.get('items'):
        return json_response.get('items')
    return []


def get_tracks_from_playlist(user_id, playlist_name):
    playlists = get_users_playlists(user_id)
    tracks = [];

    for playlist in playlists:
        if playlist['name'] == playlist_name:
            tracks = get_playlist_tracks(user_id, playlist['id'])

    # return array of tracks for a particular playlist
    if len(tracks) > 0:
        return tracks.get('items')
    return []


def get_tracks_array(user_id, playlist_name):
    tracks = [];
    playlist = get_tracks_from_playlist(user_id, playlist_name)

    if len(playlist) > 0:
        for track in playlist:
            if track['track'].get('preview_url'):
                newTrack = {}
                newTrack['name'] = track['track']['name']
                newTrack['artists'] = [name['name'] for name in track['track']['artists']]
                newTrack['preview_url'] = track['track']['preview_url']
                newTrack['popularity'] = track['track']['popularity']
                newTrack['image_url'] = track['track']['album']['images'][1]
                tracks.append(newTrack)
    
    return tracks

##### RANDOM PLAYLIST FUNCTIONS #####

def get_random_playlists():
    # generate a list of 10 popular playlists
    playlists = [
        "3ZgmfR6lsnCwdffZUan8EA", "37i9dQZF1DX0XUsuxWHRQd", "5SMf1pyrOAwjwheZvHWkaj", "37i9dQZF1EQpj7X7UK8OOF", "37i9dQZF1EQnqst5TRi17F", 
        "37i9dQZF1DX9qNs32fujYe", "0J74JRyDCMotTzAEKMfwYN", "37i9dQZF1EQqkOPvHGajmW", "1h0CEZCm6IbFTbxThn6Xcs", "01mtswy9f2A3ayUFB2Aynv"
    ]
    random_playlists = []

    for playlist in playlists:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "limit": '500',
                "offset": '0'
            }
        )
        response_json = response.json()
        if response_json['tracks']:
            random_playlists.append(response_json)

    return random_playlists 

def get_tracks_from_rand_playlist(playlist_name):
    playlists = get_random_playlists()
    tracks = [];

    for playlist in playlists:
        if playlist['name'] == playlist_name:
            tracks = get_rand_playlist_tracks(playlist['id'])

    # return array of tracks for a particular playlist
    if len(tracks) > 0:
        return tracks.get('items')
    return []

def get_random_tracks_array(playlist_name):
    tracks = [];
    playlist = get_tracks_from_rand_playlist(playlist_name)

    if len(playlist) > 0:
        for track in playlist:
            if track['track'].get('preview_url'):
                newTrack = {}
                newTrack['name'] = track['track']['name']
                newTrack['artists'] = [name['name'] for name in track['track']['artists']]
                newTrack['preview_url'] = track['track']['preview_url']
                newTrack['popularity'] = track['track']['popularity']
                newTrack['image_url'] = track['track']['album']['images'][1]
                tracks.append(newTrack)
    
    return tracks
