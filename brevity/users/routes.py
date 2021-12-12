from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from brevity import db, bcrypt
from brevity.models import Bookmark, User, Post
from brevity.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from brevity.users.utils import save_picture, send_reset_email                     
from brevity.main.forms import SearchForm
import time


users = Blueprint('users', '__name__')

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')        
    return render_template('login.html', title='Login', form=form)
    
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():                       # if the request method is 'POST' then we need to redirect 
                                                        # instead of returning a web page directly.
                                                        # so that when we reload, the form doesn't get resubmitted. (POST/REDIRECT/GET pattern)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                            image_file = image_file, form = form)


@users.route("/user/posts/<string:username>")
def user_posts(username):
    form=SearchForm()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (Post.query.filter_by(author = user)
        .order_by(Post.date_posted.desc())
        .paginate(page = page, per_page = 5)
        )
    return render_template('user_posts.html', posts=posts, form=form, user=user)


@users.route("/user/more_posts/<string:username>/<int:page>")
def more_user_posts(username, page):
    user = User.query.filter_by(username=username).first_or_404()
    posts = (Post.query.filter_by(author = user)
        .order_by(Post.date_posted.desc())
        .paginate(page = page, per_page = 5)
        )
    time.sleep(.3)
    return render_template('user_posts_loop_partial.html', posts=posts, user=user, page=page)

 
@users.route("/user/bookmarks/<string:username>")
def bookmarked_posts(username):
    form=SearchForm()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    bookmarked_posts = Bookmark.query.filter_by(user_id=user.id).with_entities(Bookmark.post_id)
    posts = (Post.query.filter(Post.id.in_(bookmarked_posts))
                .order_by(Post.date_posted.desc())
                .paginate(page = page, per_page = 5)
            )
    return render_template('bookmarked_posts.html', posts=posts, form=form, user=user)


@users.route("/user/more_bookmarks/<string:username>/<int:page>")
def more_bookmarked_posts(username, page):
    user = User.query.filter_by(username=username).first_or_404()
    bookmarked_posts = Bookmark.query.filter_by(user_id=user.id).with_entities(Bookmark.post_id)
    posts = (Post.query.filter(Post.id.in_(bookmarked_posts))
                .order_by(Post.date_posted.desc())
                .paginate(page = page, per_page = 5)
            )
    time.sleep(.3)            
    return render_template('bookmarked_posts_loop_partial.html', posts=posts, user=user, page=page)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)