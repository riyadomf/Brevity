from flask import render_template, request, Blueprint
from brevity.models import Post

main = Blueprint('main', '__name__')

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


