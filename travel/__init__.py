# I have created file __init__.py. to tell Python that my directory is a package.
# This file initializes my application and brings together different components

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager
from flask_ckeditor import CKEditor

# Configure application
app = Flask(__name__)

# Set up SECRET KEY in order to use CSRF token
# Random string generated using secrets.token_hex(16)
app.config['SECRET_KEY'] = '789cda65e3f57b4fdedee8d71a2e6f01'

# Initialize CKEditor
ckeditor = CKEditor(app)

# Configure database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from travel import views # this is done at the end in order to avoid circular import