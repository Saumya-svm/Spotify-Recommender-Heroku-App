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

1. Ideation
   The basic idea for the application was to recommend a group of users new music they can groove to collectively. There can be several ways users can connect with music. It can be through instrumentals, genres, lyrics , context etc. The first(and the most basic) version of the app will connect users through instumentals, audio features such as acousticness, tempo, valence etc. The reason this is the most basic version is because it does not take into account semantics or artist/genre preference. These additional factors can significantly wiegh in a user's music taste. Also, the songs are not classified based on genres in the current version. The recommednations will be purely based on audio features made available by Spotify R&D through Spotify Web API./
2. Data Collection
   token, api
3. Data Cleaning
4. How to get recommendations?
5. Deployment


---

Readme todo-

* About the project
* Tech used in the project
* Steps followed in the project

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

## Resources
