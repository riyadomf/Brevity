from datetime import datetime
from enum import unique
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy.orm import backref 
from brevity import db, login_manager
from brevity.posts.forms import CommentForm
from flask_login import UserMixin, current_user


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
    upvoted = db.relationship('Upvote', foreign_keys='Upvote.user_id', backref='user', lazy='dynamic')
    downvoted = db.relationship('Downvote', foreign_keys='Downvote.user_id', backref='user', lazy='dynamic')
    commented = db.relationship('Comment', backref='author', lazy=True)      

    def upvote_post(self, post):
        if not self.has_upvoted_post(post):
            upvote = Upvote(user_id=self.id, post_id=post.id)
            db.session.add(upvote)
            if self.has_downvoted_post(post):
                Downvote.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
        else:
            Upvote.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_upvoted_post(self, post):
        return Upvote.query.filter(
            Upvote.user_id == self.id,
            Upvote.post_id == post.id).count() > 0


    def downvote_post(self, post):
        if not self.has_downvoted_post(post):
            downvote = Downvote(user_id=self.id, post_id=post.id)
            db.session.add(downvote)
            if self.has_upvoted_post(post):
                Upvote.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
        else:
            Downvote.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_downvoted_post(self, post):
        return Downvote.query.filter(
            Downvote.user_id == self.id,
            Downvote.post_id == post.id).count() > 0
    


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

    tags = db.relationship('Tag', backref='post', cascade="all, delete", lazy='dynamic')
    upvotes = db.relationship('Upvote', backref='post', lazy='dynamic')
    downvotes = db.relationship('Downvote', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    resources = db.relationship('ResourceFile', backref='post', lazy='dynamic')       

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
                                                                                    #author can be used in Post object and it returns a User object.

class Tag(db.Model):
    tag = db.Column(db.String(50), nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

class Upvote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)


class Downvote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)


class Comment(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"
    
class ResourceFile(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True)
    filename = db.Column(db.String(50), nullable = False, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    