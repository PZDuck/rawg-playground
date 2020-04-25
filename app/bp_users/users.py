from flask_login import  login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, url_for, Blueprint, session
from app.forms import RegForm, LoginForm, CreateCollectionForm
from app.db_collections import load_user, User
from app import app

import requests

bp_users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


# Registration/Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            user = User.objects(email=form.email.data).first()
            if not user:
                new_user = User.register(email=form.email.data, password=form.password.data, username=form.username.data)
                login_user(new_user)
                return redirect('/')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect('/')
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            user = User.authenticate(email=form.email.data, password=form.password.data)
            if user:
                login_user(user)
                session['saved_games'] = [key for key in current_user.saved_games.keys()]
                return redirect('/')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# User account page
@app.route('/account')
@login_required
def account():
    games = []
    for game_id in list(current_user.saved_games.keys()):
        games.append(requests.get(f'https://api.rawg.io/api/games/{game_id}').json())

    form = CreateCollectionForm()

    return render_template('account.html', user=current_user, games=games, form=form)



def get_game(game_id):
    return requests.get(f'https://api.rawg.io/api/games/{game_id}').json()