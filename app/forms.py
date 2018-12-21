from flask_wtf import Form
''' define forms for flask app '''

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
