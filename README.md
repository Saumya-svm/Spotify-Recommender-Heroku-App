## About

Ever Partying with your friends and wondering what songs will make everyone groove? Ever going on a road trip and wondering what music will make everyone enjoy the journey?
Well worry no more!
Introducing the Spotify buddy classifier.
This Recommendation system will use your playlist and your friend’s playlist and combine them to make the perfect curated playlist consisting of songs that cater to the tastes of both you and your friend.

**Here’s how to get the perfect playlist in 6 simple steps:**

Step 1- Please enter your own playlist in space given. Your playlist can be private or public as you have already logged into your Spotify account and we can access your Spotify playlist with the Spotify web API

Step 2- Please enter your friend’s playlist. Your friend’s playlist needs to be public as we cannot access their private playlists.

Step 3- Please enter the name you would give to your new playlist.

Step 4- Please enter the description you would like to give to your new playlist.

Step 5- Please click on generate after filling all the inputs. This will redirect you to your newly generated playlist.

Step 6- Enjoy!

Visit here: http://buddyplaylistgenerator.herokuapp.com/

Since, I am yet to get approval to my quota extension from Spotify, kindly mail me if you want to test the application.

Mail:saumyamundra@gmail.com

---

## Features

* **Generate Playlist**
  This feature generates a playlist for you and your friend based on your music taste. Right now it is based on a very basic idea of cosine similarity, however we will explore more methods(genre analysis and more audio features) and more song data to provide better recommendations.
* **Add Tracks**
  This will help you add new tracks to any of your playlists in your profile. The main aim is to add songs to the new generated playlist, along with the songs which were already present.
* **Get Playlist**
  Will display all your playlists and help you explore it. This feature is still in development mode, as we will analyse and explore paterns it in the upcoming versions of the project

## Roadmap

* **Ideation:**
  The basic idea for the application was to recommend a group of users new music they can groove to collectively. There can be several ways users can connect with music. It can be through instrumentals, genres, lyrics , context etc. The first(and the most basic) version of the app will connect users through instumentals, audio features such as acousticness, tempo, valence etc. The reason this is the most basic version is because it does not take into account semantics or artist/genre preference. These additional factors can significantly wiegh in a user's music taste. Also, the songs are not classified based on genres in the current version. The recommednations will be purely based on audio features made available by Spotify R&D through Spotify Web API.
* **Data Collection:**
  The songs dataset can be collected from [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge). You can create an account on AIcrowd to download the data from the resources section. We would not get individual songs from the file, rather there will be a thousand json files which will store songs in a playlist format.
  Accessing all the files will take a siginificant amount of time. Finally, we want a dataset wich contains songs along with their audio features, which have to be accessed through the Spotify Web API. Initially, we only have data abotu songs, with some metadata.While collecting the data from the files, I interrupted the process in the early stages due to time and computation limitations. Despite this, I had  collected metadata for about 2 million songs. The next step was to access the 'Get Audio Features' endpoint. We would have to provide  the song 'id' as the only parameter. The 'requests' library can be used, but we would have to define the endpoint url,  headers, parameters etc. by ourself. If one is unfamiliar with API calls, 'spotipy' library is there to the rescue. We can use the 'spotipy' library to get audio features for our tracks. An object will be created by passing an access token to the 'auth' parameter. The newly created object  can call various functions offering multiple functionalities. For our use case, the `audio_features()` function will get us the features for each track.

```
{
        "name": "musical",
        "collaborative": "false",
        "pid": 5,
        "modified_at": 1493424000,
        "num_albums": 7,
        "num_tracks": 12,
        "num_followers": 1,
        "num_edits": 2,
        "duration_ms": 2657366,
        "num_artists": 6,
        "tracks": [
            {
                "pos": 0,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:7vqa3sDmtEaVJ2gcvxtRID",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Finalement",
                "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
                "duration_ms": 166264,
                "album_name": "Dancing Chords and Fireflies"
            },
            {
                "pos": 1,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:23EOmJivOZ88WJPUbIPjh6",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Betty",
                "album_uri": "spotify:album:3lUSlvjUoHNA8IkNTqURqd",
                "duration_ms": 235534,
                "album_name": "Endless Smile"
            },
            {
                "pos": 2,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:1vaffTCJxkyqeJY7zF9a55",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Some Beat in My Head",
                "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
                "duration_ms": 268050,
                "album_name": "Dancing Chords and Fireflies"
            },
            // 8 tracks omitted
            {
                "pos": 11,
                "artist_name": "Mo' Horizons",
                "track_uri": "spotify:track:7iwx00eBzeSSSy6xfESyWN",
                "artist_uri": "spotify:artist:3tuX54dqgS8LsGUvNzgrpP",
                "track_name": "Fever 99\u00b0",
                "album_uri": "spotify:album:2Fg1t2tyOSGWkVYHlFfXVf",
                "duration_ms": 364320,
                "album_name": "Come Touch The Sun"
            }
        ],

    }
```

* Data Cleaning
* How to get recommendations?
* Deployment

---

## Tools

Languages - Python, HTML, CSS

Frameworks/Libraries - Flask, Spotipy, Scikit Learn, Pandas, Numpy, Gspread

API's - Spotify Web API

## References

**Data**

The data was downloaded from Spotify's R&D webpage. You will be redirected to AIcrowd where you would have to create an account to download the data.

(https://dl.acm.org/doi/abs/10.1145/3240323.3240342):
*Ching-Wei Chen, Paul Lamere, Markus Schedl, and Hamed Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018.*

## Getting Started

To run this app on your local machine,

* Clone the repository

  ```
  git clone https://github.com/Saumya-svm/Spotify-Recommender-Heroku-App
  ```
* Install required packages/tools

  ```
  pip install -r requirements.txt
  ```
* Run the app

  ```
  python run.py
  ```
