from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import  FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tag = StringField('Tag')
    fileResource = MultipleFileField('Upload Resources',
                    validators=[FileAllowed(['jpg', 'png', 'pdf', 'xlsx'])])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')