from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import  FileAllowed
from brevity.posts.utils import FileSizeLimit


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tag = StringField('Tag')
    fileResource = MultipleFileField('Upload Resources',
                    validators=[FileAllowed(['jpg', 'png', 'pdf', 'xlsx']), FileSizeLimit(max_size_in_mb=4)])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')