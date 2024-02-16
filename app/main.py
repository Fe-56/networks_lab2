from fastapi import FastAPI, Request, Response
from typing import Optional
from utils import *

# import the model files
from models.user import User
from models.playlist import Playlist

app = FastAPI()

# root
@app.get("/")
def root():
    return "A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"

# create user
@app.post("/users")
def create_user(user: User, response: Response):
    user_id = user.userID
    name = user.name
    password = user.password
    error = 0

    # validation
    if is_valid_string(user_id, name, password):
        if (has_space(user_id) or has_space(password)):
            error = 1
        elif user_exists(user_id):
            error = 2
        else:
            add_user(user)
            return f"Hello {name}! Your userID is {user_id} and password is {password}, please remember them!"
    else:
        error = 3

    # error handling
    if error != 0:
        response.status_code = 400

        if error == 1:
            return "Please ensure that your userID and/or password have no whitespaces or spaces!"
        elif error == 2 :
            return f"UserID {user_id} taken! Please provide another userID!"
        elif error == 3:
            return "Please ensure that you enter the userID and/or name and/or password as valid strings in the request body as a JSON!"
        
# retrieve songs
@app.get("/songs")
def retrieve_song(response: Response, sortBy: Optional[str] = None, count: Optional[int] = None):
    error = 0

    # validation
    if not is_valid_sortby(sortBy):
        error = 1
    elif not is_valid_count(count):
        error = 2
    else:
        return retrieve_songs(sortBy, count)
    
    # error handling
    if error != 0:
        response.status_code = 400

        if error == 1:
            return "Please ensure that your sortBy query is either artist or title!"
        elif error == 2:
            return "Please ensure that your count query is more than or equals to 1!"

# create playlist
@app.post("/playlists/{user_id}/{password}")
def create_playlist(user_id: str, password: str, playlist: Playlist, response: Response):
    playlist_id = playlist.playlistID
    title = playlist.title
    description = playlist.description
    error = 0

    # validation
    if not user_exists(user_id):
        error = 1
    else:
        # authorisation
        if not password_correct(user_id, password):
            error = 2

        else: 
            if is_valid_string(playlist_id, title, description):
                if has_space(playlist_id):
                    error = 3
                else:
                    if playlist_exists(playlist_id):
                        error = 4
                    elif is_valid_playlist(playlist):
                        add_playlist(user_id, playlist)
                        return f"Your playlist with playlistID {playlist_id} has been created!"
                    else:
                        error = 5
            else:
                error = 6

    # error handling
    if error == 1:
        response.status_code = 404
        return f"userID {user_id} is not found! Please enter an existing userID!"
    elif error == 2:
        response.status_code = 401
        return f"The password provided is wrong! Please provide a valid password for userID {user_id}"
    else:
        response.status_code = 400

        if error == 3:
            return "Please ensure that your playlistID has no whitespaces or spaces!"
        elif error == 4:
            return f"Playlist {playlist_id} already exists! Please provide another playlistID!"
        elif error == 5:
            return "Please ensure that the songID(s) that you enter in the songs list are all valid and exists in the songs database!"
        elif error == 6:
            return "Please ensure that you enter the playlistID and/or title and/or description as valid strings in the request body as a JSON!"
        
# retrieve playlist
@app.get("/playlists/{user_id}/{playlist_id}")
def retrieve_playlist(user_id: str, playlist_id: str, response: Response):
    error = 0

    # validation
    if not user_exists(user_id):
        error = 1
    elif not playlist_exists(playlist_id):
        error = 2
    else:
        return get_playlist(playlist_id)
    
    # error handling
    if error != 0:
        response.status_code = 404

        if error == 1:
            return f"userID {user_id} is not found! Please enter an existing userID!"
        elif error == 2:
            return f"playlistID {playlist_id} is not found! Please enter an existing userID!" 
        
# update playlist
@app.put("/playlists/{user_id}/{password}/{playlist_id}")
def update_playlist(user_id: str, password: str, playlist_id: str, new_playlist: Playlist, response: Response):
    new_playlist_id = new_playlist.playlistID
    new_title = new_playlist.title
    new_description = new_playlist.description
    error = 0

    # validation
    if not user_exists(user_id):
        error = 1
    else:
        # authorisation
        if not password_correct(user_id, password):
            error = 2
        else: 
            if not playlist_exists(playlist_id):
                error = 3
            else:
                if is_valid_string(new_playlist_id, new_title, new_description):
                    if has_space(new_playlist_id):
                        error = 4
                    else:
                        if is_valid_playlist(new_playlist):
                            update_playlist_in_db(playlist_id, new_playlist)
                            return f"Your playlist, originally with playlistID {playlist_id}, has been updated to a new playlist with new playlistID {playlist_id}!"
                        else:
                            error = 5
                else:
                    error = 6

    # error handling
    if error == 1 or error == 3:
        response.status_code = 404
        
        if error == 1:
            return f"userID {user_id} is not found! Please enter an existing userID!"
        elif error == 3:
            return f"Playlist with playlistID {playlist_id} does not exist! Please enter an existing playlistID!"
    elif error == 2:
        response.status_code = 401
        return f"The password provided is wrong! Please provide a valid password for userID {user_id}"
    else:
        response.status_code = 400
        
        if error == 4:
            return "Please ensure that your playlistID has no whitespaces or spaces!"
        elif error == 5:
            return "Please ensure that the songID(s) that you enter in the songs list are all valid and exists in the songs database!"
        elif error == 6:
            return "Please ensure that you enter the playlistID and/or title and/or description as valid strings in the request body as a JSON!"
        
# batch update playlists
@app.put("/batch_update/playlists/{user_id}/{password}")
async def batch_update_playlist(user_id: str, password: str, request: Request, response: Response):
    request_json = await request.json()
    error = 0

    # validation
    if not user_exists(user_id):
        error = 1
    else:
        # authorisation
        if not password_correct(user_id, password):
            error = 2
        else:
            if not is_valid_json(request_json):
                error = 3
            else:
                song_id = request_json["songID"]

                if not song_exists(song_id):
                    error = 4
                else :
                    num_of_updated_playlists, updated_playlists = delete_song_from_playlists(user_id, song_id)
                    
                    if num_of_updated_playlists == 0:
                        error = 5
                    else:
                        return f"Song with songID {song_id} deleted from the following playlists belonging to userID {user_id}: {updated_playlists}"
            
    # error handling
    if error == 1 or error == 4:
        response.status_code = 404

        if error == 1:
            return f"userID {user_id} is not found! Please enter an existing userID!"
        elif error == 4:
            return f"Song with songID {song_id} does not exist in the songs database! Please enter an existing songID!"
    elif error == 2:
        response.status_code = 401
        return f"The password provided is wrong! Please provide a valid password for userID {user_id}"
    elif error == 3 or 5:
        response.status_code = 400
        
        if error == 3:
            return f"Invalid request JSON! Please ensure that it only has a single key, called `songID`, and that the value assigbned to it is a string!"
        elif error == 5:
            return f"No playlists belonging to userID {user_id} has the songID {song_id} in it!"
        
admin_password = "lab2"
        
@app.get("/admin/users")
async def get_users(request: Request, response: Response):
    request_admin_password = request.headers.get('admin-password')

    # authorisation
    if request_admin_password != admin_password:
        response.status_code = 401
        return "Wrong admin password!"
    else:
        return get_users_db()

@app.get("/admin/playlists")
def get_playlists(request: Request, response: Response):
    request_admin_password = request.headers.get('admin-password')

    # authorisation
    if request_admin_password != admin_password:
        response.status_code = 401
        return "Wrong admin password!"
    else:
        return get_playlists_db()
