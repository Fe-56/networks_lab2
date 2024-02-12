# Networks Lab 2 - REST API Documentation
## By: Lim Fuo En [1005125]

This REST API imitates a Spotify-like service.
It can create users and playlists, list (read) playlists and songs, and also update playlists.

## Note
This documentation consists of how to build and run my code and how to make HTTP requests to my API, as well as the expected responses for each request.

<ins>It also contains a section (all the way at the end) that identifies the idempotent routes in my application.</ins>

## Setup
Simply run `docker compose up` and make sure you get "A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2" by sending a GET request to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Making HTTP requests to this API
I would recommend you to use Postman to send the HTTP request to this REST API. Please use [this link](https://dark-flare-820920.postman.co/workspace/My-Workspace~480f5cea-c01c-44d6-8540-e62907c4f2b6/collection/15698908-c7bb7f73-adee-4a7e-937e-1b8be35058e5?action=share&creator=15698908) to access the Postman collection with all the API endpoints already properly set up and ready for you to modify (the request body and headers of) and send to this REST API.

Else, you may use your preferred method to send the HTTP requests. Just read the following section for the list of endpoints you can make requests to and ensure that the response you receive coincides with the expected responses.

## Expected responses for each request
### 1) Root
#### Request:
```
GET http://127.0.0.1:8000/ HTTP/1.1
```
#### Expected Response:
```
STATUS: 200 OK
"A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"
```
### 2) Create User
#### Request:
```
POST http://127.0.0.1:8000//users/create HTTP/1.1
Content-Type: application/json

{
  "userID": "string",
  "name": "string",
  "password": "string"
}
```
Please ensure that there are no spaces/white spaces in `userID` and `password`.
#### Expected Response:
```
STATUS: 200 OK
"Hello {name}! Your userID is {userID} and password is {password}, please remember them!
```

### 3) Retrieve Songs
#### Request:
```
GET http://127.0.0.1:8000/songs?sortBy={sortBy}&count={count} HTTP/1.1
```
Please ensure that `sortBy` is either "artist", "title", or "album".
#### Expected Response:
```
{
    {songID}: {
        "songID": {songID},
        "title": "string",
        "artist": "string",
        "album": "string"
    }
    ...
    ...
    ...
}
```
Where `songID` is a string.

#### Expected Response:
```
"Hello {name}! Your userID is {userID} and password is {password}, please remember it!"
```

### Create Playlist
#### Request:
```
POST http://127.0.0.1:8000//playlists/{userID}/{password}/create HTTP/1.1
Content-Type: application/json

{
    "playlistID": "string",
    "title": "string",
    "description": "string",
    "songs": [
        "string"
    ]
}
```
Please enter the `songID` of the song(s) in the list of strings for the key value of "songs" in the JSON request body.
#### Expected Response:
```
STATUS: 200 OK
"Your playlist with {playlistID} has been created!
```

### 4) Retrieve Playlist
#### Request:
```
GET http://127.0.0.1:8000/playlists/{userID}/{playlistID} HTTP/1.1
```
#### Expected Response:
```
STATUS: 200 OK
{
    {playlistID}: {
        "playlistID": {playlistID},
        "title": "string",
        "description": "string",
        "userID": {userID},
        "dateTimeCreated": "datetime"
        "dateTimeModified": "datetime",
        "songs": [
            "string"
        ]
    }
}
```

### 5) Update Playlist
#### Request:
```
PUT http://127.0.0.1:8000/playlists/{userID}/{password}/{playlistID} HTTP/1.1
Content-Type: application/json

{
    "playlistID": {newPlaylistID},
    "title": "string",
    "description": "string",
    "songs": [
        "string"
    ]
}
```
Where `newPlaylistID` is a string.
#### Expected Response:
```
STATUS: 200 OK
"Your playlist, originally with playlistID {playlistID}, has been updated to new playlist with new playlistID {newPlaylistID}}!"
}
```

### 6) Batch Update Playlists
#### Request:
```
PUT http://127.0.0.1:8000/batch_update/playlists/{userID}/{password}?songID={songID} HTTP/1.1
Content-Type: application/json

{
    "songID": {songID}
}
```
Where `songID` is a string.
#### Expected Response:
```
STATUS: 200 OK
"Song with songID {song_id} has been deleted from the following playlists belonging to userID {userID}: {updated_playlists}"
```

### 7) Get All Users
#### Request:
```
GET -h "admin-password: {adminPasword}" http://127.0.0.1:8000/admin/users HTTP/1.1
```
Where the `adminPassword` is `lab2`.
#### Expected Response:
```
STATUS: 200 OK
"A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"
```

### 8) Get All Playlists
#### Request:
```
GET -h "admin-password: {adminPassword}" http://127.0.0.1:8000/admin/playlists HTTP/1.1
```
Where the `adminPassword` is `lab2`.
#### Expected Response:
```
STATUS: 200 OK
"A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"
```

## Idempotent routes in this application

