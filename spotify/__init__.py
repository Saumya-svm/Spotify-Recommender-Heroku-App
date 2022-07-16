from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '90124236a7d47951b60d4bb689990f5e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
client_id = 'c6defb694a6c4ee4a9c083967cf87fe2';
client_secret = '13ce694f6d9a422f82818b86752e85e9'; 
redirect_uri = 'http://localhost:7777/callback'; 
app.config['CLIENT_ID'] = client_id
app.config['CLIENT_SECRET'] = '13ce694f6d9a422f82818b86752e85e9'
app.config['REDIRECT_URI'] = 'http://localhost:7777/callback'
# app.config['SCOPE'] = 'playlist-modify-private user-read-recently-played playlist-modify-public'
app.config['SCOPE'] = 'playlist-read-private playlist-modify-public playlist-modify-private user-read-recently-played playlist-read-collaborative'
app.config['access_token'] = ''

db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from spotify import routes