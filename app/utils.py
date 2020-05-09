import os
from . import app
from flask_login import current_user
from werkzeug.utils import secure_filename

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
            avatar.save(os.path.join(app.config['IMAGE_UPLOADS'], current_user.username, 'avatar', filename))

            return os.path.join('\static', 'users', current_user.username, 'avatar', filename)
    
    return None

def upload_collection_img(request):
    if request.files:
        image = request.files['collection_image']

        if allowed_img(image.filename):

            image.filename = '.'.join((f'{current_user.username}_{request.form["collection_name"]}', image.filename.split('.')[1]))
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], current_user.username, 'collections', filename))

            return os.path.join('\static', 'users', current_user.username, 'collections', filename)
    
    return None