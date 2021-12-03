import os, secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename




def save_file(form_file):
    random_hex = secrets.token_hex(8)                                           # To randomize the name of the uploaded image so that the name doesn't collide with the already uploaded ones 
    _, f_ext = os.path.splitext(secure_filename(form_file.filename))            # Splits the filename and extension in 2 part.
                                            # We don't need the filename. That's why we represent it with '_'.
                                            #     To let the editor know that it's unused.
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static', 'resource_files', file_fn )
    
    form_file.save(file_path)

    return file_fn