from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.forms import RegForm, LoginForm, SearchForm
from app.db_collections import load_user, User
from . import app, db
import json, requests


'''
Main routes
'''

# Index Page
@app.route('/')
def index():
    top_rated = requests.get('https://api.rawg.io/api/games?page_size=10').json()
    games = top_rated['results']
    return render_template('index.html', games=games)

# Contact Us Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Search Page with the Search Form
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    publishers = requests.get('https://api.rawg.io/api/publishers?page_size=40').json()
    form.publishers.choices += [(i['id'], i['name']) for i in publishers['results']]

    genres = requests.get('https://api.rawg.io/api/genres?ordering=-games_count').json()
    form.genres.choices += [(i['id'], i['name']) for i in genres['results']]

    return render_template('search.html', form=form)

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
        return jsonify(user)
    
    user.save_game(data['id'], data['status'])
    session['saved_games'] = list(user.saved_games.keys())
    return jsonify(user)

# Create a new empty collection for the current user
@app.route('/create-collection', methods=['POST'])
@login_required
def create_collection():
    data = request.get_json()
    collection = data['data']
    user = User.objects(email=current_user.email).first()
    print(collection)
    user.create_collection(collection['collection_name'], collection['collection_description'], collection['collection_image'], collection['date_created'])
    return jsonify(user)

# Add a particular game to the current user's collection
@app.route('/add-to-collection', methods=['POST'])
@login_required
def add_to_collection():
    data = request.get_json()
    user = User.objects(email=current_user.email).first()
    user.add_game_to_collection(data['data']['game_id'], data['data']['collection_name'])
    return jsonify(user)
