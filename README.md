# Networks Lab 2 - REST API Documentation
## By: Lim Fuo En [1005125]

This REST API imitates a Spotify-like service.
It can create users and playlists, list (read) playlists and songs, and also update playlists.

## Note
This documentation consists of how to build and run my code and how to make HTTP requests to my API, as well as the expected responses for each request.

<ins>It also contains a section (all the way at the end) that identifies the idempotent routes in my application.</ins>

## Setup
In the root project directory, run `docker compose up` and make sure you get "A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2" by sending a GET request to [http://127.0.0.1:8000](http://127.0.0.1:8000).

You may want to first review the .json files in `./app/data` folder [here](https://github.com/Fe-56/networks_lab2/tree/master/app/data). These .json files contain the data that will be initialised in the playlists, songs, and users databases, and some of the request endpoints in my REST API deals with some of the initialised data.

## Making HTTP requests to this API
I would recommend you to use Postman to send the HTTP request to this REST API. Please use [this link](https://dark-flare-820920.postman.co/workspace/My-Workspace~480f5cea-c01c-44d6-8540-e62907c4f2b6/collection/15698908-c7bb7f73-adee-4a7e-937e-1b8be35058e5?action=share&creator=15698908) to access the Postman collection with all the API endpoints already properly set up and ready for you to modify (the request body and headers of) and send to this REST API.

Else, you may use your preferred method to send the HTTP requests. Just read the following section for the list of endpoints you can make requests to and ensure that the response you receive coincides with the expected responses.

## Expected responses for each request
Please note that for the sub-sections on "Error Responses", it is assumed that you did not leave out any field in the JSON request body and entered the correct data type as stated in the "Request" sub-section.
***
### 1) Root
***
This request simply checks whether the code for this REST API is correctly built and run.
#### Request:
```
GET http://127.0.0.1:8000/ HTTP/1.1
```
#### Expected Response:
```
STATUS: 200 OK
"A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"
```
***
### 2) Create User
***
This request creates a new user resource and inserts it into the users database.
#### Request:
```
POST http://127.0.0.1:8000/users HTTP/1.1
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
#### Error Responses:
##### If there is whitespace in the provided `userID` and/or `password`:
```
STATUS: 400 Bad Request
"Please ensure that your userID and/or password have no whitespaces or spaces!"
```
***
### 3) Retrieve Songs
***
This request retrieves a list of songs available in the songs database. It is able sort the songs and limit the number of songs in the response.
#### Request:
```
GET http://127.0.0.1:8000/songs?sortBy={sortBy}&count={count} HTTP/1.1
```
Please ensure that `sortBy` is either `artist`, `title`, or `album`, and that `count` is an integer greater than or equal to 1.
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
#### Error Responses:
##### If the `sortBy` query is anything other than `artist` or `title`:
```
Status: 400 Bad Request
"Please ensure that your sortBy query is either artist or title!"
```
##### If the `count` query is an integer lesser than 1:
```
Status: 400 Bad Request
"Please ensure that your count query is more than or equals to 1!"
```
***
### 4) Create Playlist
***
This request creates a new playlist resource and inserts it into the playlists database.
#### Request:
```
POST http://127.0.0.1:8000/playlists/{userID}/{password} HTTP/1.1
Content-Type: application/json

{
    "playlistID": {playlistID},
    "title": "string",
    "description": "string",
    "songs": [
        "string"
    ]
}
```
Please ensure that there are no whitespaces in the `playlistID` as provided in the JSON request body.\
Please enter the `songID` of the song(s) in the list of strings for the value of the `songs` attribute in the JSON request body.\
Please ensure that the `songID` exists in the songs datbase. Note that `playlistID` is a string. 
#### Expected Response:
```
STATUS: 200 OK
"Your playlist with {playlistID} has been created!
```
#### Error Responses:
##### If a non-existent `userID` is provided:
```
Status: 404 Not Found
"userID {userID} is not found! Please enter an existing userID!"
```
##### If a wrong `password` is provided:
```
Status: 401 Unauthorized
"The password provided is wrong! Please provide a valid password for userID {userID}"
```
##### If an existing `playlistID` is provided:
```
Status: 400 Bad Request
"Playlist {playlistID} already exists! Please provide another playlistID!"
```
##### If an invalid/non-existent `songID` within the `songs` field is provided:
```
Status: 400 Bad Request
"Please ensure that the songID(s) that you enter in the songs list are all valid and exists in the songs database!"
```
##### If there is whitespace in the provided `playlistID`:
```
STATUS: 400 Bad Request
"Please ensure that your playlistID have no whitespaces or spaces!"
```
***
### 5) Retrieve Playlist
***
This request retrieves the playlist with a playlistID that matches the provided `playlistID`.\
This request can be used to check if a new playlist resource has indeed been created by teh request 4) Create Playlist.
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
#### Error Responses:
##### If a non-existent `userID` is provided:
```
Status: 404 Not Found
"userID {userID} is not found! Please enter an existing userID!"
```
##### If a non-existent `playlistID` is provided:
```
Status: 404 Not Found
"playlistID {playlistID} is not found! Please enter an existing playlistID!"
```
***
### 6) Update Playlist
***
This request updates a single playlist resource that matches the provided `playlistID` with the new playlist information as provided in the JSON request body.
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
Where `newPlaylistID` is a string. Please ensure that there are no white spaces in the `newPlaylistID` as provided in the JSON request body. Please enter the `songID` of the song(s) in the list of strings for the value of the `songs` attribute in the JSON request body. Please ensure that the `songID` exists in the songs database.
#### Expected Response:
```
STATUS: 200 OK
"Your playlist, originally with playlistID {playlistID}, has been updated to a new playlist with new playlistID {newPlaylistID}}!"
```
#### Error Responses:
##### If a non-existent `userID` is provided:
```
Status: 404 Not Found
"userID {userID} is not found! Please enter an existing userID!"
```
##### If a wrong `password` is provided:
```
Status: 401 Unauthorized
"The password provided is wrong! Please provide a valid password for userID {userID}"
```
##### If a non-existing `playlistID` is provided:
```
Status: 404 Not Found
"Playlist with playlistID {playlistID} does not exist! Please enter an existing playlistID!"
```
##### If an invalid/non-existent `songID` within the `songs` field is provided:
```
Status: 400 Bad Request
"Please ensure that the songID(s) that you enter in the songs list are all valid and exists in the songs database!"
```
##### If there is whitespace in the provided `newPlaylistID`:
```
STATUS: 400 Bad Request
"Please ensure that your playlistID have no whitespaces or spaces!"
```
***
### 7) Batch Update Playlists
***
**Challenge:** This special request batch updates all available playlists of the user `userID` with the provided `songID` in its `songs` field, by deleting the `songID` in the `songs` field.
#### Request:
```
PUT http://127.0.0.1:8000/batch_update/playlists/{userID}/{password} HTTP/1.1
Content-Type: application/json

{
    "songID": {songID}
}
```
Where `songID` is a string. Please ensure that the provided `songID` exists in the songs database, and it is currently in an existing playlist.
#### Expected Response:
```
STATUS: 200 OK
"Song with songID {song_id} has been deleted from the following playlists belonging to userID {userID}: {updated_playlists}"
```
#### Error Responses:
##### If a non-existent `userID` is provided:
```
Status: 404 Not Found
"userID {userID} is not found! Please enter an existing userID!"
```
##### If a wrong `password` is provided:
```
Status: 401 Unauthorized
"The password provided is wrong! Please provide a valid password for userID {userID}"
```
##### If an invalid/non-existent `songID` is provided:
```
Status: 404 Not Found
"Song with songID {songID} does not exist in the songs database! Please enter an existing songID!"
```
##### If a valid `songID` is provided, but it does not belong to any playlist belonging to `userID`:
```
Status: 400 Bad Request
"No playlists belonging to userID {userID} has the songID {songID} in it!"
```
***
### 8) Get All Users
***
This admin request retrieves all available users from the users database.\
This request can be used to check if a new user resource has indeed been created by the request 2) Create User.\
**Challenge:** This request has a form of authorisation that inspects the request headers.
#### Request:
```
GET -h "admin-password: {adminPasword}" http://127.0.0.1:8000/admin/users HTTP/1.1
```
Where the `adminPassword` is `lab2`.\
`adminPassword` is a request header.
#### Expected Response:
```
STATUS: 200 OK
{
  {userID}: {
    "userID": {userID},
    "name": "string",
    "password": "string"
  }
  ...
}
```
#### Error Responses:
##### If the wrong `adminPassword` is provided:
```
Status: 401 Unauthorized
"Wrong admin password!"
```
***
### 9) Get All Playlists
***
This admin request retrieves all available playlists from the playlists database.\
This request can be used to check if a new playlist resource has indeed been created by the request 4) Create Playlist.\
**Challenge:** This request has a form of authorisation that inspects the request headers.
#### Request:
```
GET -h "admin-password: {adminPassword}" http://127.0.0.1:8000/admin/playlists HTTP/1.1
```
Where the `adminPassword` is `lab2`.\
`adminPassword` is a request header.
#### Expected Response:
```
STATUS: 200 OK
{
    {playlistID}: {
        "playlistID": {playlistID},
        "title": "string",
        "description": "string",
        "userID": "string",
        "dateTimeCreated": "datetime"
        "dateTimeModified": "datetime",
        "songs": [
            "string"
        ]
    }
    ...
}
```
#### Error Responses:
##### If the wrong `adminPassword` is provided:
```
Status: 401 Unauthorized
"Wrong admin password!"
```

## Idempotent routes in this application
Idempotent routes are routes that can be requested many times without changing the result. The following are the routes that I identified as idempotent:
***
### 1) Root
***
```
GET http://127.0.0.1:8000/ HTTP/1.1
```
#### Why is it idempotent?
This route simply returns the same, fixed string without any regard for any request parameters.
***
### 3) Retrieve Songs
***
```
GET http://127.0.0.1:8000/songs?sortBy={sortBy}&count={count} HTTP/1.1
```
#### Why is it idempotent?
This route returns the same list of songs, as long as the `sortBy` and `count` are the same.

This is because this route does not insert or delete any song from the songs database. It simply validates the `sortby` and `count` from the request, and then reads songs from the database.

Therefore, it is idempotent and you will always get the same result.
***
### 5) Retrieve Playlist
***
```
GET http://127.0.0.1:8000/playlists/{userID}/{playlistID} HTTP/1.1
```
#### Why is it idempotent?
This route returns the same playlist JSON, as long as the provided `playlistID`, `userID`, and `password` are the same.

This is because this route does not insert or delete any playlist from the playlists database, and does not modify them too. It simply validates that the `userID` exists in the users database, and that there exists a playlist in the playlists database with the provided `playlistID`.

Therefore, it is idempotent and you will always get the same result, as long as you do not modify the playlists before sending a request to this route.
***
### 8) Get All Users
***
```
GET -h "admin-password: {adminPasword}" http://127.0.0.1:8000/admin/users HTTP/1.1
```
#### Why is it idempotent?
This route returns all the user JSON in the users database, as long as you provide the correct `adminPassword` of `lab2`.

This is because this route does not insert, delete, or modify any user from the users database. It simply validates that the provided `adminPassword` is correct, and returns all the user JSON available.

Therefore, it is idempotetent and you will always get the same result.
***
### 9) Get All Playlists
***
```
GET -h "admin-password: {adminPassword}" http://127.0.0.1:8000/admin/playlists HTTP/1.1
```
#### Why is it idempotent?
This route returns all the playlist JSON in the playlists database, as long as you provide the correct `adminPassword` of `lab2`.

This is because this route does not insert, delete, or modify any playlist from the playlists database. It simply validates that the provided `adminPassword` is correct, and returns all the playlist JSON available.

Therefore, it is idempotetent and you will always get the same result.
