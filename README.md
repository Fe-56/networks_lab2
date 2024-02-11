# Networks Lab 2 - REST API Documentation
## By: Lim Fuo En [1005125]

This REST API imitates a Spotify-like service.
It can create users and playlists, list (read) playlists and songs, and also update playlists.

## Setup
Simply run `docker compose up` and make sure you get "A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2" by going to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Making HTTP requests to this API
I would recommend you to use Postman to send the HTTP request to this REST API. Please use [this link](https://dark-flare-820920.postman.co/workspace/My-Workspace~480f5cea-c01c-44d6-8540-e62907c4f2b6/collection/15698908-c7bb7f73-adee-4a7e-937e-1b8be35058e5?action=share&creator=15698908) to access the Postman collection with all the API endpoints already properly set up and ready for you to modify (the request body of) and send.

Else, you may use your preferred to send the HTTP requests. Just read the following section for the list of endpoints you can make requests to and ensure that the response you receive coincides with the expected responses.

## Expected responses for each request
### Root
#### Request:
```
GET http://127.0.0.1:8000/
```
#### Expected Response:
```
STATUS: 200 OK
"A Spotify-like REST API by Lim Fuo En [1005125] for 50.012 - Networks Lab 2"
```
### Create User
#### Request:
```
POST http://127.0.0.1:8000//users/create 
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
"Hello {name}! Your userID is {userID} and password is {password}, please remember it!"
```

### Create Playlist
#### Request:
```
POST
```
#### Expected Response:
```

```

### Retrieve Platylist
#### Request:
```
GET
```
#### Expected Response:
```

```

### Retrieve Songs
#### Request:
```
GET
```
#### Expected Response:
```

```

### Update Playlist
#### Request:
```
PUT
```
#### Expected Response:
```

```

### Batch Update Playlists
#### Request:
```
PUT
```
#### Expected Response:
```

```

## Idempotent routes in this application

