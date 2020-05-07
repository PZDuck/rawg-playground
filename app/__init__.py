from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

import os

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test_database',
    'host': 'mongodb://localhost:27017/test_database'
}
app.config['SECRET_KEY'] = 'yasosalmenyaebalidvajdi'
app.config['IMAGE_UPLOADS'] = os.path.join(os.getcwd(), 'app', 'static', 'avatars') 
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'BMP']

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views, db_collections

from .bp_users.users import bp_users
app.register_blueprint(bp_users)
