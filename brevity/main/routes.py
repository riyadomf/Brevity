from re import template
from flask import render_template, request, Blueprint
from brevity.main.utils import search_result
from brevity.models import Post, Upvote
from brevity.main.forms import SearchForm
from brevity import db
from sqlalchemy import func
import time


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




@main.route("/feed/more_posts/<int:page>")
def more_posts(page: int):
    posts = Post.query.paginate( page=page, per_page=5)
    time.sleep(.3)                                        #sleep to prove infinite scrolling
    return render_template("posts_loop_partial.html", posts=posts, page=page)





@main.route("/about")
def about():
    return render_template('about.html', title = 'About')

### sort by date(type_sort=1)
### sort by popularity(type_sort=2)
### otherwise(type_sort=0)
### search type tag(type=1)
### search type else(type=0)

@main.route('/search',methods=['GET', 'POST'])
@main.route('/search/<int:type_sort>',methods=['GET', 'POST'])
def search(type_sort=0):
    page = request.args.get('page', 1, type=int) 

    if type_sort==0:
        posts =  Post.query.paginate(page=page, per_page=5)
    elif type_sort==1:
        posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    elif type_sort==2:
        posts = db.session.query(Post).join(Upvote).filter(Post.id==Upvote.post_id).group_by(Post.id).order_by(func.count(Post.id).desc()).paginate(page=page, per_page=5)

    form=SearchForm()
    if form.validate_on_submit():
        searched_val = form.searched.data
        if searched_val==None:
            return render_template('searched_post.html', posts = posts,form_val=form.searched.data)
        return render_template('searched_posts.html', posts = search_result(searched_val,page,0),form =form,form_val=form.searched.data)

    searched_val = request.args.get('form_val')
    if searched_val==None:
        return render_template('searched_posts.html', posts = posts,form_val=searched_val)
   
    type =  request.args.get('type')

    if type=="1":
        searched_val += ']'
        searched_val = '[' + searched_val

    return render_template('searched_posts.html', posts = search_result(searched_val,page,type_sort),form =form,form_val=searched_val)


