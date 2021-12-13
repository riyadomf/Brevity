from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
from brevity.posts.utils import FileSizeLimit, MultiFileAllowed
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # content = TextAreaField('Content', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    tag = StringField('Tag')
    fileResource = MultipleFileField('Upload Resources',
                    validators=[MultiFileAllowed(['jpg', 'png', 'pdf', 'xlsx', 'txt']), FileSizeLimit(max_size_in_mb=4)])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')