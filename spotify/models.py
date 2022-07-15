from spotify import db, login_manager
from flask_login import  UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # tracks = db.relationship('Tracks', backref='tracks')
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    user1 = db.Column(db.String())
    user2 = db.Column(db.String())
    uri = db.Column(db.String())
    link = db.Column(db.String())

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String())
    name2 = name1 + name1
