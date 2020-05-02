from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.forms import RegForm, LoginForm, SearchForm, EditProfileForm
from app.db_collections import load_user, User, Collection
from . import app, db
import json, requests


'''
Main routes
'''

# Index Page
@app.route('/', methods=['GET', 'POST'])
def index():
    top_rated = requests.get('https://api.rawg.io/api/games?page_size=10').json()
    games = top_rated['results']
    
    form = SearchForm()

    publishers = requests.get('https://api.rawg.io/api/publishers', params={ 'page_size': 40 }).json()
    form.publishers.choices += [(i['id'], i['name']) for i in publishers['results']]

    genres = requests.get('https://api.rawg.io/api/genres', params={ 'ordering': '-games_count' }).json()
    form.genres.choices += [(i['id'], i['name']) for i in genres['results']]

    return render_template('index.html', games=games, form=form)

# Contact Us Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

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

# Detail Page for a particular Game
@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_details(game_id):
    game = requests.get(f'https://api.rawg.io/api/games/{game_id}').json()
    screenshots = requests.get(f'https://api.rawg.io/api/games/{game_id}/screenshots').json()
    suggested = requests.get(f'https://api.rawg.io/api/games/{game_id}/suggested').json()
    return render_template('details.html', game=game, screenshots=screenshots, suggested=suggested)

# Collection page
@app.route('/collections/<username>/<collection>', methods=['GET', 'POST'])
def collection_details(username, collection):
    user = User.objects(username=username).first()
    collection = user.collections[collection]
    games = []
    for game_id in collection['games']:
        games.append(requests.get(f'https://api.rawg.io/api/games/{game_id}').json())
    return render_template('collection.html', collection=collection, games=games)


'''
Routes used by JS Axios
'''

# Get list of games after the search form has been submitted
@app.route('/get-games', methods=['POST'])
def get_games():
    data = request.get_json()
    url = data['data']['url']
    params = data['data']['params']
    resp = requests.get(url, params=params)
    return resp.json()

# Save a particular game to the current user's list of saved games
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

# Create a new empty collection for the current user
@app.route('/create-collection', methods=['POST'])
@login_required
def create_collection():
    data = request.get_json()
    collection = data['data']
    
    user = User.objects(email=current_user.email).first()
    user.create_collection(collection['collection_name'], collection['collection_description'], collection['collection_image'], collection['date_created'])
    Collection.create_collection(user['email'], collection['collection_name'], collection['collection_description'], collection['collection_image'])
 
    return "OK", 200

# Add a particular game to the current user's collection
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
