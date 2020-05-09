from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SelectField, DateField, TextAreaField, FormField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Email, Length, Optional

import datetime


class RegForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=64)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Optional()])
    publishers = SelectField('Publishers', choices=[('', '')], validators=[Optional()])
    genres = SelectField('Genres', choices=[('', '')], validators=[Optional()])
    order_by = SelectField('Order', choices=[('', ''), ('name', 'Alphabetic Order'), ('-name', 'Reversed Alphabetic Order'), ('released', 'Old'), ('-released', 'Recent'), ('rating', 'Least Rated'), ('-rating', 'Top Rated') ])

class CreateCollectionForm(FlaskForm):
    collection_name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField(validators=[Optional()])
    date_created = DateField(format='%Y-%m-%d', default=datetime.date.today(), render_kw={'disabled':''})

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[Optional()])
    name = StringField('Real Name', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    avatar = FileField(validators=[Optional()])