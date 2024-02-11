from fastapi import FastAPI, Response
from typing import Optional
import json
from utils import *

# import the model files
from models.user import User
from models.playlist import Playlist

users = json.load(open('./data/users.json'))
songs = json.load(open('./data/songs.json'))
playlists = json.load(open('./data/playlists.json'))

app = FastAPI()

# root
@app.get("/")
def root():
    return "A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"

# create user
@app.post("/users/create")
def create_user(user: User, response: Response):
    user_id = user.userID
    name = user.name
    password = user.password
    error = 0

    # validation
    if user_id and name and password:
        if (has_space(user_id) or has_space(password)):
            error = 1
        elif user_id in users:
            error = 2
        else:
            users[user.userID] = user
            return f"Hello {name}! Your userID is {user_id} and password is {password}, please remember it!"
    else:
        error = 3

    # error handling
    if error != 0:
        response.status_code = 400

        if error == 1:
            return "Please ensure that your userID and/or password have no whitespaces or spaces!"
        elif error ==2 :
            return f"UserID {user_id} taken! Please use another userID!"
        elif error == 3:
            return "Please ensure that you enter the userID and/or name and/or password in the request body as a JSON!"

# create playlist
@app.post("/playlists/{user_id}/{playlist_id}")
def create_playlist(user_id: str, playlist_id: str):
    return {
        
    }

# FOR TESTING
@app.get("/test/users")
def get_users():
    return users

@app.get("/test/playlists")
def get_playlists():
    return playlists
