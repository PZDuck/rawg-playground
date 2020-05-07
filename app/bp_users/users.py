from flask_login import  login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, url_for, Blueprint, session, redirect, jsonify
from werkzeug.utils import secure_filename
from app.forms import RegForm, LoginForm, CreateCollectionForm, EditProfileForm
from app.db_collections import load_user, User, Collection
from app import app

import requests
import os

bp_users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


# UTIL FUNCTIONS

def allowed_img(filename):
    print(filename)
    if not '.' in filename:
        return False
    
    ext = filename.split('.')[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    
    return False

def upload_avatar(request):
    if request.files:
        avatar = request.files['avatar']

        if allowed_img(avatar.filename):

            avatar.filename = '.'.join((f'{current_user.username}_avatar', avatar.filename.split('.')[1]))
            filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config['IMAGE_UPLOADS'], current_user.username, filename))

            return os.path.join('\static', 'avatars', current_user.username, filename)
    
    return None

    
# Registration/Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(email=form.email.data).first()
            if not user:
                new_user = User.register(email=form.email.data, password=form.password.data, username=form.username.data)
                os.makedirs(f'{app.config["IMAGE_UPLOADS"]}/{form.username.data}')
                login_user(new_user)
                return redirect('/')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect('/')
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
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
@app.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def account(username):

    if current_user.username == username:
        games = {'wtp': [], 'cp': [], 'finished': []}
        user_games = list(current_user.saved_games.keys())
        for game in user_games:
            games[current_user.saved_games[game]].append(requests.get(f'https://api.rawg.io/api/games/{game}').json())


        collection_form = CreateCollectionForm(obj=current_user)
        profile_form = EditProfileForm(obj=current_user)

        if request.method == 'POST':

            if profile_form.validate_on_submit():
                avatar_url = upload_avatar(request)
                current_user.update_profile(profile_form.data['name'], profile_form.data['city'], avatar_url)
                return render_template('account_own.html', user=current_user, games=games, collection_form=collection_form, profile_form=profile_form)
    
        return render_template('account_own.html', user=current_user, games=games, collection_form=collection_form, profile_form=profile_form)
    
    else:
        user = User.objects(username=username).first()

        games = {'wtp': [], 'cp': [], 'finished': []}
        user_games = list(user.saved_games.keys())
        for game in user_games:
            games[user.saved_games[game]].append(requests.get(f'https://api.rawg.io/api/games/{game}').json())
        
        public_collections = Collection.objects(username=username, is_private=False).all()

        return render_template('account.html', user=user, games=games, collections=public_collections)


