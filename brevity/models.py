from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app 
from brevity import db, login_manager
from flask_login import UserMixin


                                                                                    #we need to provide a user_loader callback. This callback is used to 
                                                                                    #  reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))      
                                                                                    #User class needs to implement 4 important property and method:
                                                                                    #  is_authenticated, is_active, is_anonymous, get_id()    
                                                                                    #To make implementing a user class easier, we can inherit from UserMixin
                                                                                    #  which provides default implementations for all of these properties and methods.
class User(db.Model, UserMixin):                                                    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)                    #By default SQLAlchemy guess the relationship to be one to many as posts returns a list of post.
                                                                                    #  If you would want to have a one-to-one relationship you can pass uselist=False to relationship().                 
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')                #user_id is the payload

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  
                                                                                    #posts works like a pseudo column. It runs additional query on the Post table to get a list of all the posts made by a user
                                                                                    #author can be used in Post object and it returns a User object.


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                                                                                    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
                                                                                    #author can be used in Post object and it returns a User object.