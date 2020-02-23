from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Enter Username"}, validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', render_kw={"placeholder": "Enter Email Address"}, validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')


class SearchForm(FlaskForm):
    term = StringField('Search', render_kw='Type to search', validators=[DataRequired(), Length(min=2,max=60)])