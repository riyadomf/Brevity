from operator import pos
from flask import render_template, request, Blueprint
from flask.helpers import url_for
from flask_sqlalchemy import Pagination
from sqlalchemy.sql.expression import desc
from flask_wtf import form
from werkzeug.utils import redirect
from brevity.main.utils import search_result
from brevity.models import Post, Tag, Upvote
from brevity.main.forms import SearchForm
from brevity.posts.routes import post
from brevity import db
from sqlalchemy import or_
from sqlalchemy import func


main = Blueprint('main', '__name__')

@main.context_processor
def layout():
    form=SearchForm()
    return dict(form=form)

@main.route("/")
@main.route("/home/<int:type>",methods=['GET', 'POST'])
def home(type=0):
    page = request.args.get('page', 1, type=int)      # type = int : to raise value error when someone passes anything other than int.
    #posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if type==0:
        posts =  Post.query.paginate(page=page, per_page=5)
    elif type==1:
        posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    elif type==2:
        posts = db.session.query(Post).join(Upvote).filter(Post.id==Upvote.post_id).group_by(Post.id).order_by(func.count(Post.id).desc()).paginate(page=page, per_page=5)
        #posts =  Post.query.order_by(func.count(Post.upvotes)).paginate(page=page, per_page=5)
    

    return render_template('home.html', posts = posts)
                                                    #paginate() returns a pagination object which has necessary attributes and methods.
                                                    #dir(object): returns all the attributes and methods of that object

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


@main.route('/search',methods=['GET', 'POST'])
@main.route('/search/<int:type>',methods=['GET', 'POST'])
def search(type=0):
    page = request.args.get('page', 1, type=int) 

    if type==0:
        posts =  Post.query.paginate(page=page, per_page=5)
    elif type==1:
        posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    elif type==2:
        posts = db.session.query(Post).join(Upvote).filter(Post.id==Upvote.post_id).group_by(Post.id).order_by(func.count(Post.id).desc()).paginate(page=page, per_page=5)

    form=SearchForm()
    if form.validate_on_submit():
        searched_val = form.searched.data
        if searched_val==None:
            return render_template('searched_post.html', posts = posts,form_val=form.searched.data)
        return render_template('searched_posts.html', posts = search_result(searched_val,page),form =form,form_val=form.searched.data)

    searched_val = request.args.get('form_val')
    if searched_val==None:
        return render_template('searched_posts.html', posts = posts,form_val=searched_val)

    type =  request.args.get('type')
    if type=="1":
        searched_val += ']'
        searched_val = '[' + searched_val
    print(searched_val)
    return render_template('searched_posts.html', posts = search_result(searched_val,page),form =form,form_val=searched_val)
    
    

