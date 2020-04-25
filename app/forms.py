from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TextAreaField, FormField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Email, Length, Optional

import datetime


class RegForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(max=64)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[InputRequired()])
    publishers = SelectField('Publishers', choices=[('', '')], validators=[Optional()])
    genres = SelectField('Genres', choices=[('', '')], validators=[Optional()])
    order_by = SelectField('Order', choices=[('', ''), ('name', 'Alphabetic Order'), ('-name', 'Reversed Alphabetic Order'), ('released', 'Old'), ('-released', 'Recent'), ('rating', 'Least Rated'), ('-rating', 'Top Rated') ])

class CreateCollectionForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    description = TextAreaField('description', validators=[Optional()])
    image = URLField('image', validators=[Optional()])
    date_created = DateField(format='%Y-%m-%d', default=datetime.date.today(), render_kw={'disabled':''})