import json
from datetime import datetime, timedelta
import copy

# import the model files
from models.user import User
from models.playlist import Playlist

users = json.load(open('./data/users.json'))
songs = json.load(open('./data/songs.json'))
playlists = json.load(open('./data/playlists.json'))



# validation helper functions

# returns True if all of the input arguments are not None and have a length of more than 0, and is not just a space or spaces, input arguments can only be strings
def is_valid_string(*args):
    for string in args:
        if (not string) or (len(string) == 0) or string.isspace():
            return False
        
    return True

# returns True if the input string has any space/whitespace in it
def has_space(string):
    return " " in string

# returns True if the user exists in the users database
def user_exists(user_id):
    return user_id in users

# returns True if the provided password matches the password of the userID in the users database
def password_correct(user_id, password):
    return password == users[user_id]["password"]

# returns True if the song exists in the songs database
def song_exists(song_id):
    return song_id in songs

# returns True if the playlist exists in the playlists database
def playlist_exists(playlist_id):
    return playlist_id in playlists

# returns True if the songs provided in the songs list of the playlist exists in the songs database. meaning this function checks whether a playlist is valid
def is_valid_playlist(playlist: Playlist):
    playlist_songs = playlist.songs

    for song_id in playlist_songs:
        if not song_exists(song_id):
            return False
    
    return True

# returns the playlist from playlist_id
def get_playlist(playlist_id):
    raw_playlist = playlists[playlist_id]
    returned_playlist = copy.deepcopy(raw_playlist)
    returned_playlist["songs"] = []

    # convert the song_id to their corresponding song title
    for song_id in raw_playlist["songs"]:
        song_title = songs[song_id]["title"]
        returned_playlist["songs"].append(song_title)

    return returned_playlist

# returns True if the sortBy query of the retrieve songs endpoint is either "title" or "artist" or "album"
def is_valid_sortby(sort_by):
    return (sort_by == "title") or (sort_by == "artist") or (sort_by == "album")

# returns True if the count query of the retrieve songs endpoint is at least 1
def is_valid_count(count):
    return count >= 1

# sort the songs based on the sort_by and limit the number of retrieved songs based on limit
def retrieve_songs(sort_by, limit):
    retrieved_songs = {}
    sorted_songs = sorted(
        songs.items(),
        key = lambda song: song[1][sort_by]
    )[:limit]

    for song in sorted_songs:
        song_id = song[0]
        song_details = song[1]
        retrieved_songs[song_id] = song_details

    return retrieved_songs

# returns True if the request_json is valid for the batch update playlists endpoint
def is_valid_json(request_json):
    return ("songID" in request_json) and (type(request_json["songID"]) == str)



# database modification helper functions

# adds new user to users database
def add_user(user: User):
    new_user = {
        "userID": user.userID,
        "name": user.name,
        "password": user.password
    }
    users[user.userID] = new_user

# adds new playlist to playlists database
def add_playlist(user_id, playlist: Playlist):
    new_playlist = {
        "playlistID": playlist.playlistID,
        "title": playlist.title,
        "description": playlist.description,
        "userID": user_id,
        "dateTimeCreated": datetime.now() + timedelta(hours=8), # GMT +8, Singapore timezone
        "dateTimeModified": None,
        "songs": playlist.songs
    }
    playlists[playlist.playlistID] = new_playlist

# updates existing playlist in the playlists database
def update_playlist_in_db(playlist_id, new_playlist: Playlist):
    playlist_to_update = playlists[playlist_id]
    
    # fields to keep
    user_id = playlist_to_update["userID"]
    date_time_created = playlist_to_update["dateTimeCreated"]

    # update the playlist
    playlist_to_update["playlistID"] = new_playlist.playlistID
    playlist_to_update["title"] = new_playlist.title
    playlist_to_update["description"] = new_playlist.description
    playlist_to_update["songs"] = new_playlist.songs
    del playlists[playlist_id]
    playlists[new_playlist.playlistID] = {
        "playlistID": new_playlist.playlistID,
        "title": new_playlist.title,
        "description": new_playlist.description,
        "userID": user_id,
        "dateTimeCreated": date_time_created,
        "dateTimeModified": datetime.now() + timedelta(hours=8), # GMT +8, Singapore timezone,
        "songs": new_playlist.songs   
    }

# removes the songID from all existing playlists belonging to userID in the playlists database
def delete_song_from_playlists(user_id, song_id):
    user_playlists = []
    playlists_to_update = []
    playlists_to_update_ids = []

    for playlist_id, playlist in playlists.items():
        if playlist["userID"] == user_id:
            user_playlists.append(playlist)

    for playlist in user_playlists:
        if song_id in playlist["songs"]:
            playlists_to_update.append(playlist)

    for playlist in playlists_to_update:
        playlist_id = playlist["playlistID"]
        playlist["songs"].remove(song_id)
        playlists[playlist_id] = playlist
        playlists_to_update_ids.append(playlist_id)

    return (len(playlists_to_update_ids), ', '.join(playlists_to_update_ids))



# database retrieval helper functions
    
def get_users_db():
    return users

def get_playlists_db():
    return playlists
