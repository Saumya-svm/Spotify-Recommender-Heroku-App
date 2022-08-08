from flask import render_template, flash, redirect, url_for, request, make_response, session
from flask_login import login_user, login_required, logout_user, current_user
from spotify import app, db, bcrypt
from sklearn.linear_model import LinearRegression
import numpy as np
from spotify.models import Tracks, User
from spotify.forms import RegistrationForm, LoginForm, updateAccountForm, SearchForm, GeneratePlaylistForm
import os
from spotify.functions import createStateKey, getPlaylistsLinks, getToken, getUserInformation, getPlaylist, addtracks, search, create_playlist, getTracks, friends_comparison, getPlaylistsNames, recommend
import logging
import time
import spotipy
import pandas as pd

@app.route('/')
@app.route('/home')
def home():
    if 'img' not in session:
        session['img'] = '../static/profile_pics/default.jpg'
    if 'access_token' not in session:
        return render_template('home.html')
    else:
        return render_template('home.html', token=session['access_token'], img=session['img'])

# @app.route('/test')
# def db_test():
#     users = db.session.query(User).filter(User.username != current_user.username).all()
#     tracks = []
#     for user in users:
#         track_objects = db.session.query(Tracks).filter(Tracks.user1.in_([user.username, current_user.username]), Tracks.user2.in_([user.username, current_user.username])).all()
#         if track_objects:
#             tracks.append(track_objects)
#     return render_template('test.html', tracks=tracks)

@app.route('/test')
def test():
    sp = spotipy.Spotify(auth=session['access_token'])
    zipped = zip([1,2,3],[4,5,6])
    results = sp.user_playlist_tracks('n54f9w8gp8h635wczdm9tpgt2','3US22IIdQQl54YC7Q0IHDJ')
    return render_template('test.html', results=results, zipped=zipped)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# does form not validate if form.hidden_tag attribute is not passed
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful')
    return render_template('login.html', title='Login', form=form)


@app.route('/account')
@login_required
def account():
    form = updateAccountForm()
    users = db.session.query(User).filter(User.username != current_user.username).all()
    tracks = []
    for user in users:
        track_objects = db.session.query(Tracks).filter(Tracks.user1.in_([user.username, current_user.username]), Tracks.user2.in_([user.username, current_user.username])).all()
        if track_objects:
            tracks.append([track_objects, user])
    return render_template('account.html', tracks=tracks, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/authorize')
def authorize():
    session['next'] = ''
    next = request.args.get('next')
    session['next'] = next

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    redirect_uri = app.config['REDIRECT_URI']
    scope = 'playlist-modify-private user-read-recently-played playlist-read-private'

    # using a state key to save the app from cyber attacks
    state_key = createStateKey(16)
    session['state_key'] = state_key
    session['previous_url'] = '/home'

    authentication_url = 'https://accounts.spotify.com/authorize?'
    parameters = f'response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state_key}&show_dialog=true'
    
    response = make_response(redirect(authentication_url + parameters))
    # session['response'] = response
    return redirect(authentication_url + parameters)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    session.pop('state_key', None)
    session['access_token'] = ''
    tokens = getToken(code)
    if tokens:
        session['access_token'] = tokens[0]
        session['refresh_token'] = tokens[1]
        session['expires_in'] = time.time() + tokens[2]
    else:
        return render_template('error.html', error='Failed to access token', tokens=tokens.json())
    if session['next']:    
        next_url = url_for(session['next'])
    info = getUserInformation(session['access_token'])['images']
    if len(info) > 0:
        session['img'] = getUserInformation(session['access_token'])['images'][0]['url']
    print('next', session['next'])
    return redirect(next_url) if session['next'] else redirect(url_for('spotifyaccount'))


# decorator for accessing spotify accounts
def spotifyloginrequired(func):
    
    def wrapper(*args, **kwargs):
        # 
        if len(session['access_token']) > 0:
            # 
            return render_template('spotifyaccount.html')
        else:
            return render_template('error.html', error='Login with Spotify')

    return wrapper

@app.route('/spotifyaccount')
def spotifyaccount():
    if len(session['access_token']) > 0:
        return render_template('spotifyaccount.html', img=session['img'])
    else:
        return render_template('error.html', error='Login with Spotify')

@app.route('/spotifylogout')
def spotifylogout():
    session['access_token'] = ''
    flash('**User logged out')
    session['img'] = '../static/profile_pics/default.jpg'
    # return redirect('https://accounts.spotify.com/en/logout')
    return render_template('home.html', img=session['img'])

@app.route('/getplaylist', methods=['GET', 'POST'])
def getplaylist():
    response = getPlaylistsLinks(session['access_token'])
    searchBoolean = 0
    playlist_ids = response
    if not response:
        return render_template('error.html', error=response)
    else:
        form = SearchForm()
        tracks = []
        links = []
        playlist_ids = getPlaylistsLinks(session['access_token'])
        playlist_names = getPlaylistsNames(session['access_token'])
        name_id_zip  = zip(playlist_names, playlist_ids)
        if form.validate_on_submit():
            searchBoolean = 1
            search_response = search(session['access_token'], form.search.data)
            for item in search_response:
                tracks.append(['open.spotify.com/track/'+item['id'], item['id'], item['name'], item['artists'][0]['name'], [playlist_ids], playlist_names])
                links.append(item['id'])
    return render_template('getPlaylist.html',links=links, tracks=tracks, form=form, ids=playlist_ids, zip=name_id_zip, searchBoolean=searchBoolean)

@app.route('/generated')
def generated():
    idd = session['created_id']
    return render_template('generated.html', id=idd)

def get_id(link):
    id = link.split('/')[-1]
    if '?' in id:
        print(id[:id.index('?')])
    return id[:id.index('?')]


@app.route('/generateplaylist', methods=['GET', 'POST'])
def generateplaylist():
    form = GeneratePlaylistForm()
    playlist_ids = []
    tracks_uri = []
    searchform = SearchForm()
    searchboolean = False
    prediction = ''
    session['access_token'] = session.get('access_token', '')
    if len(session['access_token']) == 0:
        return redirect(url_for('authorize', next=request.endpoint))
    else:
        try:
            if form.validate_on_submit():
                searchboolean = True
                id1 = get_id(form.playlist_id1.data)
                id2 = get_id(form.playlist_id2.data)
                name = form.playlist_name.data
                description = form.playlist_description.data
                
                playlist_ids = [id1, id2]
                for playlist_id in playlist_ids:
                    tracks_uri.extend(getTracks(session['access_token'], playlist_id))
                """"

                after getting the playlists links we will run a recommender system and get the tracks with their uri

                """
                # getting recommendations
                # concat the links
                recommended_tracks = recommend(id1, id2, session['access_token'])
                # recommended_tracks = list(pd.read_csv('Recommender/test_uri.csv')['uri'].values)
                user_id = getUserInformation(session['access_token'])['id']
                playlist_id = create_playlist(session['access_token'], user_id, name, description)
                session['created_id'] = playlist_id
                playlist_ids = [playlist_id]
                print(addtracks(session['access_token'], playlist_id, recommended_tracks, 500))
                return redirect(url_for('generated'))
        except:
            flash("**Kindly provide links to Playlists which are public. We cannot access other user's private playlist.")
        return render_template('generateplaylist.html', form=form, ids=playlist_ids, searchform=searchform, searchboolean=searchboolean, prediction=prediction)


@app.route('/about')
def about():
    return render_template('about.html')

def save_picture(file):
    _, extension = os.path.splitext(file.filename)
    name = current_user.username + extension
    path = os.path.join('../static/profile_pics/', name)
    file.save(path)
    return name

@app.route('/updateaccount', methods=['GET', 'POST'])
def update_account():
    form = updateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        username = current_user.username
        tracks = db.session.query(Tracks).filter((Tracks.user1 == username) | (Tracks.user2 == username)).all()
        current_user.username = form.username.data
        current_user.email = form.email.data
        for track in tracks:
            if track.user1 == username:
                track.user1 = current_user.username
            else:
                track.user2 = current_user.username
        db.session.commit()
        flash('Account Updated')
        return redirect(url_for('account'))
    return render_template('updateAccount.html', form=form)

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/searchTracks', methods=['GET', 'POST'])
def searchTracks():
    if len(session['access_token']) > 0:
        form = SearchForm()
        tracks = []
        links = []
        playlist_ids = [getPlaylistsLinks(session['access_token'])]
        playlist_names = getPlaylistsNames(session['access_token'])
        name_id_zip  = zip(playlist_names, playlist_ids)
        if form.validate_on_submit():
            search_response = search(session['access_token'], form.search.data)
            for item in search_response:
                tracks.append(['open.spotify.com/track/'+item['id'], item['id'], item['name'], item['artists'][0]['name'], playlist_ids, playlist_names])
                links.append(item['id'])
    else:
        return render_template('error.html', error='Login with Spotify')
    return render_template('addTracks.html', form=form, tracks=tracks, links=links, playlist_ids = playlist_ids, zip=name_id_zip)

@app.route('/add/<string:playlist_id>/<string:track_add>', methods=['GET', 'POST'])
def add(playlist_id, track_add):
    track_add = ['spotify:track:'+track_add]
    response = addtracks(session['access_token'], playlist_id, track_add)
    if response.status_code == 201:
        flash('**Track added. It might take time for the track to show in the embedded playlists below due to limitations fropm Spotify. However, your songs will be added in the playlist in your Spotify Account :)')
        return redirect(url_for('searchTracks'))
    else:
        flash('**Track not added')
        return redirect(url_for('searchTracks'))