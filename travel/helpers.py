'''
Huge shoutout to Corey Schafer.
His Python Flask Tutorial series:
https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
was insanely helpful in creating the whole project,
 especially this file and database models it contains
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
from travel import db, login_manager
from flask_login import UserMixin
from flask_ckeditor import CKEditorField

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

###############
#### FORMS ####
###############

# Class for creating registration forms
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Class for creating login forms
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Class for creating NEW POST forms
class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')

# Class for changing password form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Your New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

def validate_username(self, username):
    if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


#########################
#### DATABASE MODELS ####
#########################


'''
UserMixin is a subclass from Flask-Login. UserMixin allows to use methods
such as is_authenticated(), is_active(), is_anonymous(), and get_id ().
If we don't include the UserMixin in our User model, we'll get errors like
'User' object has no attribute 'is_active'.
'''

# Class for adding new users to a database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # backref allows to connect posts to users

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Class for adding new posts to a database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

