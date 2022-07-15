from logging import PlaceHolder
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField, EmailField, FileField
from wtforms.validators import DataRequired,Length, Email,EqualTo, ValidationError
from flask_login import current_user
from spotify.models import User

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Account with the username already exists. Register with another username.')

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class updateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Upload Image File', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Account with the username already exists. Update with another username.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Account with the email already exists. Update with another email.')
    

class SearchForm(FlaskForm):
    search = StringField('Enter Track', validators=[DataRequired()])
    enter = SubmitField('Enter')

class GeneratePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist Title', render_kw={"placeholder":"The playlist will be assigned a default name if the field is blank"})
    playlist_description = StringField('Playlist Description', render_kw={"placeholder":"The playlist will be assigned a default name if the field is blank"})
    playlist_public = BooleanField('Make the Playlist Public')
    playlist_id1 = StringField('Personal Playlist Link (Optional)', render_kw={"placeholder": "Enter playlist link you think might represent you best. If you want songs from all your playlists to be considered in evaluating your music taste, leave this blank"})
    playlist_id2 = StringField("Friend's Playlist Link", validators=[DataRequired()], render_kw={"placeholder":"Link a playlist that best represents your buddy(can input playlist links from their account)"})

    submit = SubmitField('Generate')