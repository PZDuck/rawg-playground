from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.forms import RegForm, LoginForm, SearchForm, EditProfileForm
from app.db_collections import load_user, User, Collection
from app.utils import allowed_img, upload_collection_img
from . import app, db
import json, requests


"""

Main routes

"""

# Landing Page
@app.route('/', methods=['GET', 'POST'])
def index():
    top_rated = requests.get('https://api.rawg.io/api/games?page_size=10').json()
    games = top_rated['results']
    
    form = SearchForm()

    publishers = requests.get('https://api.rawg.io/api/publishers', params={ 'page_size': 40 }).json()
    form.publishers.choices += [(i['id'], i['name']) for i in publishers['results']]

    genres = requests.get('https://api.rawg.io/api/genres', params={ 'ordering': '-games_count' }).json()
    form.genres.choices += [(i['id'], i['name']) for i in genres['results']]

    public_collections = Collection.objects(is_private=False).all()

    return render_template('index.html', games=games, form=form, collections=public_collections)

# Search Page with the Search Form
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    publishers = requests.get('https://api.rawg.io/api/publishers', params={ 'page_size': 40 }).json()
    form.publishers.choices += [(i['id'], i['name']) for i in publishers['results']]

    genres = requests.get('https://api.rawg.io/api/genres', params={ 'ordering': '-games_count' }).json()
    form.genres.choices += [(i['id'], i['name']) for i in genres['results']]

    args = {}
    for i in request.args:
        args[i] = request.args[i]

    return render_template('search.html', form=form, args=args)

# Game Detail Page
@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_details(game_id):
    game = requests.get(f'https://api.rawg.io/api/games/{game_id}').json()
    screenshots = requests.get(f'https://api.rawg.io/api/games/{game_id}/screenshots').json()
    suggested = requests.get(f'https://api.rawg.io/api/games/{game_id}/suggested').json()
    
    return render_template('details.html', game=game, screenshots=screenshots, suggested=suggested)

# Collection Page
@app.route('/collections/<username>/<collection>', methods=['GET', 'POST'])
def collection_details(username, collection):
    user = User.objects(username=username).first()
    collection = user.collections[collection]
    
    games = []
    for game_id in collection['games']:
        games.append(requests.get(f'https://api.rawg.io/api/games/{game_id}').json())
    
    return render_template('collection.html', collection=collection, games=games, user=user)


"""

Routes used by JS Axios
* /get-games returns a json of games matching the given parameters
* /save-game adds the game to current user's list of saved games as a key
and adds the game's state (finished, currently playing, want to play) as a value
* /create-collection creates a new collection in both User and Collection schemas
* /add-to-collection adds a game to the selected collection's games list (for User schema only)
* /delete-collection deletes the collection from both User and Collection schemas
* /toggle-private changes the state of is_private state for both User and Collection schemas

"""

@app.route('/get-games', methods=['POST'])
def get_games():
    data = request.get_json()
    
    url = data['data']['url']
    params = data['data']['params']
    
    resp = requests.get(url, params=params)
    
    return resp.json()

@app.route('/save-game', methods=['POST'])
@login_required
def save_game():
    resp = request.get_json()
    
    data = resp['data']
    user = User.objects(email=current_user.email).first()
    
    if data['id'] in user.saved_games.keys():
        del user.saved_games[data['id']]
        user.save()
        session['saved_games'] = list(user.saved_games.keys())
        return "OK", 200
    
    user.save_game(data['id'], data['status'])
    session['saved_games'] = list(user.saved_games.keys())
    
    return "OK", 200

@app.route('/create-collection', methods=['POST'])
@login_required
def create_collection():
    data = request.form
    image = upload_collection_img(request)

    user = User.objects(email=current_user.email).first()
    user.create_collection(data['collection_name'], data['collection_description'], image, data['date_created'])
    Collection.create_collection(user['email'], current_user['username'], data['collection_name'], data['collection_description'], image)
 
    return "OK", 200

@app.route('/add-to-collection', methods=['POST'])
@login_required
def add_to_collection():
    data = request.get_json()
    
    user = User.objects(email=current_user.email).first()
    user.add_game_to_collection(data['data']['game_id'], data['data']['collection_name'])
    
    return "OK", 200

@app.route('/delete-collection', methods=['POST'])
@login_required
def delete_collection():
    data = request.get_json()

    user = User.objects(email=current_user.email).first()
    user.delete_collection(data['data']['collection'])
    Collection.delete_collection(user['email'], data['data']['collection'])

    return "OK", 200

@app.route('/toggle-private', methods=['POST'])
@login_required
def toggle_private():
    data = request.get_json()

    user = User.objects(email=current_user.email).first()
    user.toggle_private(data['data']['collection_name'])
    Collection.toggle_private(data['data']['collection_name'])

    return "OK", 200