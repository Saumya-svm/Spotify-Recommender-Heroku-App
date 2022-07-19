
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
  The songs dataset can be collected from [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge). You can create an account on AIcrowd to download the data from the resources section. We would not get individual songs from the file, rather there will be a thousand json files which will store songs in a playlist format. Accessing all the files will take a siginificant amount of time. Finally, we want a dataset wich contains songs along with their audio features, which have to be accessed through the Spotify Web API. Initially, we only have data about songs, with some metadata.While collecting the data from the files, I interrupted the process in the early stages due to time and computation limitations. Despite this, I had  collected metadata for about 2 million songs. The songs were stored in a Pandas dataframe and then later exported out as a csv file. The next step was to access the 'Get Audio Features' endpoint. We would have to provide  the song 'id' as the only parameter. The 'requests' library can be used, but we would have to define the endpoint url,  headers, parameters etc. by ourself. If one is unfamiliar with API calls, 'spotipy' library is there to the rescue. We can use the 'spotipy' library to get audio features for our tracks. An object will be created by passing an access token to the 'auth' parameter. The newly created object  can call various functions offering multiple functionalities. For our use case, the `audio_features()` function will get us the features for each track. The function will return a dictionary with the feautures as keys for each track. Some of the features are as follows

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

  - acousticness - represents the confidence that a song is acoustic
  - danceability - suitability of a song for dancing
  - speechiness - detects the amount of spoken words in a song

  You can read more about them [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features). Just like extracting the song data from the json files, the process of extracting audio features is memory and computationally heavy. Upon that, the access token provided by Spotify might expire in the middle of the process. The access token provided are only active for a maximum of one hour, and the extraction of features of two million songs takes a considerably lot more time than an hour. Therefore, I decided to divide the songs into batches. I could not evenly segragate the songs as the token used to expire during a batch was running. So the range of batches were quite random. Somtimes I took a batch of 4000 and somtimes 6000, 8000 etc. At the time of writing, I extracted features for about 96000 songs, out of which 12000 were duplicates. The final recommendations were made on these some 80000 songs. However, I am runnning the feature extraction script regularly to get more data. Our final dataframe will look as follows
* Data Cleaning
  While extracting songs from playlists in the JSON files, there might be cases where the same somg will be available in two different playlists and hence, duplicates might be formed in the dataset. Upon calling `duplicated()` function on our dataset, we found that there are 12000 duplicates. We can drop the duplicates using `drop_duplicate()` function. I committed a mistake of checking for duplicates only after extracting the features. I could have saved myself reasonable computational time.
* How to get recommendations?
  We will making recommendations based on the combined music tastes of two users. We have extacted their individual playlist
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
