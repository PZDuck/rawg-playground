from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine, DynamicDocument
from flask_login import UserMixin
from app import db, login_manager

import datetime

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

    
# UTIL FUNC
def slugify(name):
    name = name.lower().replace(' ', '-')
    return name


class User(UserMixin, db.DynamicDocument):
    meta = {'collection': 'users'}
    username = db.StringField(max_length=64)
    email = db.StringField(max_length=64)
    password = db.StringField()
    date_registered = db.DateTimeField(default=datetime.datetime.utcnow())
    avatar_url = db.URLField()
    collections = db.DictField()
    saved_games = db.DictField()

    @classmethod
    def register(cls, email, password, username):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = cls(email=email, password=hashed_pwd, username=username).save()
        return user
    
    @classmethod
    def authenticate(cls, email, password):
        user = cls.objects(email=email).first()
        if user:
            check = bcrypt.check_password_hash(user.password, password)
            if check:
                return user
        return False

    def save_game(self, game_id, status):
        self.saved_games[game_id] = status
        self.save()
        return self
    
    def set_game_status(self, game_id, status):
        self.saved_game[game_id] = status
        self.save()
        return self
    
    def create_collection(self, collection_name, collection_description, collection_image, date_created):
        if not collection_image:
            collection_image = 'https://avatars.mds.yandex.net/get-pdb/1935444/fab3d347-96a8-4538-94f9-138ba41df623/s1200?webp=false'
        self.collections[slugify(collection_name)] = { 'name': collection_name, 'games': [], 'description': collection_description, 'imageURL': collection_image, 'date_created': date_created }
        self.save()
        return self
    
    def delete_colelction(self, collection_name):
        del self.collections[collection_name]
        self.save()
        return self
    
    def add_game_to_collection(self, game_id, collection_name):
        if game_id not in self.collections[collection_name]['games']:
            self.collections[collection_name]['games'].append(game_id)
            self.save()
        return self
    
    def remove_game_from_collection(self, game_id, collection_name):
        self.collection[collection_name]['games'].remove(game_id)
        self.save()
        return self

