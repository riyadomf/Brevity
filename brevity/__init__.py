'''
When the package is imported, 
    __init__.py is executed automatically.
If we import something from __init__.py module then no need to write "from brevity.__init__ import x".
    writing "from brevity import x" is enough.
'''    
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, config
from flask_mail import Mail
from brevity.config import Config
import jinja_partials
from flask_migrate import Migrate


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'       #when a user attempts to access a login_required view without being logged in, Flask-Login will flash a message and redirect them to the log in view. 
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
 
                                            #init_app() - this method is written inside each extension. 
                                            # The init_app method exists so that the extension object (e.g. flask_login object) 
                                            # can be instantiated without requiring an app object. 


def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)

   

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    from brevity.main.routes import main
    from brevity.users.routes import users
    from brevity.posts.routes import posts
    from brevity.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    jinja_partials.register_extensions(app)

    return app



''' 
Before using Blueprint:
route imports app. So we first initialize app then import routes.
So that we can avoid circular import.

After using Blueprints:
route doesn't import app. We just have to register the blueprints of the routes to the app.
'''