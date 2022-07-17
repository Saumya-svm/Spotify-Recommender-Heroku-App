import json
import string
import random
import requests
from spotify import app
import logging
import base64
import spotipy as sp
import streamlit as st
import time
import spotipy
import spotipy.util as util
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import MinMaxScaler,LabelEncoder,OneHotEncoder
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
# from xgboost import XGBClassifier
import time
from collections import Counter
from imblearn.over_sampling import SMOTE
import sys



def get_playlist_tracks(username, playlist_id, token):
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_features(track_id: str, token: str) -> dict:
        sp = spotipy.Spotify(auth=token)
        try:
            features = sp.audio_features([track_id])
            return features
        except:
            return None
        

def return_playlist(token, playlist_id, username):
    tracks = get_playlist_tracks(username, playlist_id, token)

    l = []
    for i in tracks:
        l.append(i['track']['uri'].split(':')[-1])
    string_list = []
    for i in range(len(tracks)//100 + 1):
        string_list.append(','.join(l[i*100:(i+1)*100]))

    json_list = []
    for s in string_list:
        headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': f'Bearer ' + token}
        params = [('ids', s)]
        json = ''
        try:
            response = requests.get('https://api.spotify.com/v1/audio-features', 
                        headers = headers, params = params, timeout = 5)
            json = response.json()
            json_list.append(json)
        except:
            print('None')
    dataframe_list = []
    for json in json_list:
        try:
            dataframe_list.append(pd.DataFrame(json['audio_features']))
        except:
            st.write('🚨🚨 Local files detected. Upload tracks from Spotify and press R to rerun.')
            sys.exit()
    df = pd.concat(dataframe_list)
    return df
        
def clean_data(a_data,b_data,class2,class1='Saumya Mundra'):
    a_data['class'] = class1
    b_data['class'] = class2
    

    feature_list = [ 'acousticness',
           'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key',
           'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
           'time_signature', 'valence','class']
    
    a_features = a_data[feature_list]
    b_features = b_data[feature_list]

    df = pd.concat([a_features,b_features])
    X = df.iloc[:,:-1]
    y = df.iloc[:,-1]

    #print(Counter(y))
    smote = SMOTE()
    X,y = smote.fit_resample(X,y)
    #print(Counter(y))
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=1)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit(X_train[['tempo']])

    X_train['tempo'] = scaler.transform(X_train[['tempo']])
    X_test['tempo'] = scaler.transform(X_test[['tempo']])

    return X_train,X_test,y_train,y_test

def train_model(X_train,X_test,y_train,y_test,k=13):
    model = RandomForestClassifier(random_state=1)
    # model = XGBClassifier()
    fs = SelectKBest(score_func=f_classif,k=k)
    X_train_final = pd.DataFrame(fs.fit_transform(X_train,y_train),columns = X_test.columns[fs.get_support(indices=True)])
    X_test_final = X_test[X_test.columns[fs.get_support(indices=True)]]
    model.fit(X_train_final,y_train)
    return model


def make_prediction(song_id,feature_list,model, token):
    song = pd.DataFrame(get_features(track_id=song_id,token=token))[feature_list]
    final_prediction = model.predict(song)
    if final_prediction:
        return final_prediction

def friends_comparison(token, username, playlist_id1,playlist_id2,song_id='2yLa0QULdQr0qAIvVwN6B5',name1=0,name2=1):
    streamlit1 = return_playlist(token, playlist_id1, username)
    streamlit2 = return_playlist(token, playlist_id2, username)
    
    a_data = streamlit1
    b_data = streamlit2
    a_data = a_data[:-1]
    b_data = b_data[:-1]
    
    X_train,X_test,y_train,y_test = clean_data(a_data,b_data,name2,name1)
    feature_list = X_train.columns
    model = train_model(X_train,X_test,y_train,y_test)

    #song_id = '0ofHAoxe9vBkTCp2UQIavz'
    prediction = make_prediction(song_id,feature_list,model, token)
    return prediction

def get_track_attribute(row, attribute):
    return row[attribute]

def get_features(track_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None

def get_tracks(playlist_id, token):
    sp = spotipy.Spotify(auth=token)
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    count = 0
    while results['next']:
        count+=1
        # results in the args is the previous paginated result 
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_track_info(tracks, attributes=['id', 'name']):
    data = pd.DataFrame.from_dict(tracks)

    attributes = ['id', 'name']
    for i in attributes:
        data[i] = data['track'].apply(get_track_attribute, attribute=i)

    data = data[attributes]
    return data

def track_features(data, token):
    features = data['id'].apply(get_features, token=token)
    features_df = pd.DataFrame(columns=['danceability', 'energy', 'key', 'loudness', 'mode',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'type', 'uri', 'track_href', 'analysis_url',
       'duration_ms', 'time_signature'])
    for obj in features.values:
        if obj:
            features_df = features_df.append(obj, ignore_index=True)
        else:
            print(obj)

    data = pd.concat((data, features_df), axis=1, join='inner')
    return data

def drop_columns(data, columns):
    data = data.drop(columns, axis=1)

def recommend(id1, id2, token):
    test = pd.DataFrame()
    tracks1 = get_tracks(id1, token)
    tracks2 = get_tracks(id2, token)
    test = get_track_info(tracks1+tracks2)
    test = track_features(test, token)


    data_vector = pd.DataFrame()
    numerical_columns = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness','valence', 'tempo', 'duration_ms',]
    categorical_columns = ['key', 'mode', 'time_signature']
    data_vector[numerical_columns] = test[numerical_columns].mean().values.reshape(1,-1)
    data_vector[categorical_columns] = test[categorical_columns].mode()
    columns = numerical_columns+categorical_columns

    songs = pd.read_csv('./spotify/audio_features.csv')
    result = cosine_similarity(data_vector[columns], songs[columns])
    indices = np.argsort(result[0])[-40:]
    tracks_uri = list(songs.iloc[indices]['uri'].values)
    return tracks_uri

def createStateKey(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def getToken(code):
    token_url = 'https://accounts.spotify.com/api/token'
    # authorization = app.config['AUTHORIZATION']
    redirect_uri = app.config['REDIRECT_URI']
    auth_str = f"{app.config['CLIENT_ID']}:{ app.config['CLIENT_SECRET']}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {'Authorization': f'Basic {b64_auth_str}', 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    body_params = {'code': code, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
    post_response = requests.post(token_url, headers=headers, data=body_params)

    if post_response.status_code == 200:
        json = post_response.json()
        return json['access_token'], json['refresh_token'], json['expires_in']
    else:
        logging.error('getToken:' + str(post_response.status_code))
        return  post_response

def getUserInformation(token):
    api_url = '	https://api.spotify.com/v1/me'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    post_response = requests.get(api_url, headers=headers, params={})

    if post_response.status_code == 200:
        return post_response.json()
    else:
        return post_response.json()

def getPlaylist(token):
    url = 'https://api.spotify.com/v1/playlists/0Snll1WiPhWXFwcW1ydcKE'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    params = {'playlist_id' : '0Snll1WiPhWXFwcW1ydcKE'}


    post_response = requests.get(url=url, headers=headers, params={})

    if post_response.status_code == 200:
        return post_response.json()
    else:
        return post_response.json()

def getPlaylistsLinks(token):
    """
    Description : Returns playlist ids for the current user

    Args:
    token (iterable): the access token used to access private scopes through API call

    Returns: 
    list containing playlist ids
    """

    url = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json ', 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        ids = []
        for item in response['items']:
            ids.append(item['id'])
        return ids
    else:
        return 'Access Token Expired. Try to log in again.'

def getPlaylistsNames(token):
    """
    Description : Returns playlist ids for the current user

    Args:
    token (iterable): the access token used to access private scopes through API call

    Returns: 
    list containing playlist ids
    """

    url = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json ', 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        ids = []
        for item in response['items']:
            ids.append(item['name'])
        return ids
    else:
        return 'Access Token Expired. Try to log in again.'

def getTracks(token, playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    response = response.json()
    print(response)
    tracks = []
    for item in response['items']:
        tracks.append(item['track']['uri'])
    return tracks

def addtracks(token, playlist_id, tracks=["spotify:track:4iV5W9uYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M"], limit=500):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    # params = {'playlist_id' : '0Snll1WiPhWXFwcW1ydcKE'}
    data = json.dumps(tracks)
    post_response = requests.post(url=url, headers=headers, data=data)

    return post_response

def create_playlist(token, user_id, name='Generated Buddy Playlist', description='Playlist generated through Buddy Playlist Generator', public=False):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "name":name,
        "description":description,
        "public":False
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    return response.json()['id']

def search(token, search):
    #search = input()
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    params = {
        'q':search,
        'type':'track'
    }
    #data = json.dumps(data)
    response = requests.get(url, headers=headers, params=params)
    return response.json()['tracks']['items']

# token = 'BQCjcGF3MczgM8miittdVWCUO6ppR232fmuKrGuYjoaJnIDiNght0mPQUp-ggRXAhqhdpl4v-8L6yohjvj2V6kW80rtk2smRps56VRJd0G1ls41u8edNUB8Up4Ww9g9aIIsTdT-7OLG8y16QywKW3BBpi9NJxP_4TjkW38pXBfNFJIekIZV_VjUyvgpS82qKeiRKAy5ZmDJUyFT3vJCuQUsqy_HFzRlgadKdfSKtbA'
# user_id = getUserInformation(token)
# playlist_id = create_playlist(token, user_id)
# tracks = getTracks(token, '2V4o0o9VLNf2Tl4e4Bnu1D')
# print(tracks)
# print(addtracks(token, playlist_id, tracks))

# print(recommend('2ARxmDxFaeg73SxPezgYW5', '5alMyBCUda6P5LgGy57r6g', 'BQAOnFuybKb76ALb9E3piJmkuKsSyMxO8CoFSO2KifakGOEj6xHzz5keDYdWGO0t-6X4kEJuzr5azYdsYT_g2DPBRti2KWINt4j3_tRAWkTr15VwtRrsYXekhP4Y4MCbKMmejRFUk3rS4TH5onmRpwa_wPCYm6nYlm_AcrLgF6QE8uOv3bYjl0EwIheKSsA'))