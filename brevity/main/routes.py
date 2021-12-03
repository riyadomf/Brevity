from operator import pos
from flask import render_template, request, Blueprint
from flask.helpers import url_for
from flask_sqlalchemy import Pagination
from flask_wtf import form
from werkzeug.utils import redirect
from brevity.main.utils import search_result
from brevity.models import Post, Tag
from brevity.main.forms import SearchForm
from brevity.posts.routes import post
from brevity import db
from sqlalchemy import or_


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
    print(type)
    if type==0:
        posts =  Post.query.paginate(page=page, per_page=5)
    elif type==1:
        posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    

    return render_template('home.html', posts = posts)
                                                    #paginate() returns a pagination object which has necessary attributes and methods.
                                                    #dir(object): returns all the attributes and methods of that object

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


@main.route('/search',methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int) 
    posts =  Post.query.paginate(page=page, per_page=5)
    form=SearchForm()
    if form.validate_on_submit():
        searched_val = form.searched.data
        return render_template('searched_posts.html', posts = search_result(searched_val,page),form =form,form_val=form.searched.data)

    searched_val = request.args.get('form_val')
    
    return render_template('searched_posts.html', posts = search_result(searched_val,page),form =form,form_val=searched_val)
    
    

