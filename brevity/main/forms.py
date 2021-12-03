from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    searched = TextAreaField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')