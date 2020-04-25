from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test_database',
    'host': 'mongodb://localhost:27017/test_database'
}
app.config['SECRET_KEY'] = 'yasosalmenyaebalidvajdi'

app.config['x-rapidapi-host'] = "rawg-video-games-database.p.rapidapi.com"
app.config['x-rapidapi-key'] = "e4a0b42e90msh2c35ebcb5a109ffp111f3ejsn92fac4b0d9e7"

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views, db_collections

from .bp_users.users import bp_users
app.register_blueprint(bp_users)
