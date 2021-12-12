import os
from flask import (render_template, url_for, flash, redirect, current_app, 
                    request, abort, Blueprint, send_from_directory, abort)
from flask_login import login_required, current_user
from brevity import db
from brevity.main.forms import SearchForm
from brevity.posts.forms import CommentForm, PostForm
from brevity.models import Comment, Post, ResourceFile, Tag
from brevity.posts.utils import calculateContribution, delete_file, save_file, getTagData

posts = Blueprint('posts', '__name__')



@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)

        files_filenames = []
        for file in form.fileResource.data:
            if file:
                files_filename = save_file(file)
                files_filenames.append(files_filename)
                resourceFile = ResourceFile(filename=files_filename, post_id=post.id, post=post)
                db.session.add(resourceFile)
        tags = form.tag.data.split(",")
        for tag_value in tags:
            if(tag_value!=''):
                tag = Tag(tag=tag_value, post=post)
                db.session.add(tag)
        
        db.session.commit()
       
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post', form = form, legend='New Post')



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        #delete previous tag from database
        for tag in post.tags:
            db.session.delete(tag)

        tags = form.tag.data.split(",")
        
        # add updated tags to database
        for tag_value in tags:
            if(tag_value!=''):
                print('ekhane')
                print(tag_value)
                tag = Tag(tag=tag_value, post=post)
                db.session.add(tag)

        files_filenames = []
        for file in form.fileResource.data:
            if file:
                files_filename = save_file(file)
                files_filenames.append(files_filename)
                resourceFile = ResourceFile(filename=files_filename, post_id=post.id, post=post)
                db.session.add(resourceFile)

        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tag.data = getTagData(post)
    
    return render_template('create_post.html', title = 'Update Post', post = post,
                            form = form, legend='Update Post')


@posts.route('/post/<int:post_id>/vote/<action>', methods=['GET', 'POST'])
@login_required
def vote_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    
    if action == 'upvote':
        current_user.upvote_post(post)
        db.session.commit()
        post.author.contribution = calculateContribution(post_id)
        db.session.commit()
        return render_template('vote_section.html', post=post)

    elif action == 'downvote':
        current_user.downvote_post(post)
        db.session.commit()
        post.author.contribution = calculateContribution(post_id)
        db.session.commit()
        return render_template('vote_section.html', post=post)

    elif action =='unauthorized_upvote':
        current_user.upvote_post(post)
        db.session.commit()
        post.author.contribution = calculateContribution(post_id)
        db.session.commit()
        return redirect(request.referrer)

    elif action == 'unauthorized_downvote':
        current_user.downvote_post(post)
        db.session.commit()
        post.author.contribution = calculateContribution(post_id)
        db.session.commit()
        return redirect(request.referrer)

    elif action == 'bookmark':
        current_user.bookmark_post(post)
        db.session.commit()
        return render_template('vote_section.html', post=post)


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])            #'int:' imposes that post_id must be int.
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)                               #get(id) is used to query the db through Primary key. 
                                                                        #get_or_404(id) to return 404 error instead of None in case of missing entry.
    
    comments = Comment.query.filter_by(post_id = post_id)
        
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', title="post.title",form = form, post=post, comments = comments)





@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/post/get_resource/<filename>")
def get_resource(filename):
    form = SearchForm()
    try:
        file_path = os.path.join(current_app.root_path, 'static', 'resource_files')
        return send_from_directory(directory=file_path, path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@posts.route("/post/delete_resource/<int:resource_id>", methods=['GET', 'POST'])
@login_required
def delete_resource(resource_id):
    resource = ResourceFile.query.get_or_404(resource_id)
    post = resource.post

    delete_file(resource.filename)

    db.session.delete(resource)
    db.session.commit()
    flash('Your file has been deleted!', 'success')
    return redirect(url_for('posts.update_post', post_id=post.id))




@posts.route("/post/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author != current_user:
        abort(403)
    PostId = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.post', post_id=PostId))