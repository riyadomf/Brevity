import os, secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from brevity import mail
from flask_login import current_user
from werkzeug.utils import secure_filename


def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)       # To randomize the name of the uploaded image so that the name doesn't collide with the already uploaded ones 
    _, f_ext = os.path.splitext(secure_filename(form_picture.filename))   # Splits the filename and extension in 2 part.
                                            # We don't need the filename. That's why we represent it with '_'.
                                            #     To let the editor know that it's unused.
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fn )
    
    output_size = (125,125)
    i = Image.open(form_picture)            # PIL package
    i.thumbnail(output_size)
    i.save(picture_path)
                                            # Delete previous picture while uploading new one.
    prev_picture = os.path.join(current_app.root_path,'static','profile_pics',current_user.image_file)   
    if os.path.exists(prev_picture) and os.path.basename(prev_picture)!='default.jpg':
        os.remove(prev_picture)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@brevity.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)                           #_external=True: in order to get absolute url instead of relative url.

