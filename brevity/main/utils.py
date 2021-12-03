

from brevity.models import Post, Tag
from brevity import db

def search_result(searched_val,page):
    search = "%{}%".format(searched_val)

    type=1

    sz = len(searched_val)
    if searched_val[0]=='[' and searched_val[sz-1]==']':
        type=0
    if searched_val[0]=='[' and type==0:
        searched_val = searched_val[1:]
    sz = len(searched_val)
    if searched_val[sz-1]==']' and type==0:
        searched_val = searched_val[:sz-1]
    print(searched_val)

    if type==0:
        posts = db.session.query(Post).join(Tag).filter(Post.id==Tag.post_id).filter(Tag.tag==searched_val).paginate(page=page, per_page=5)
    else:
        posts = Post.query.filter(Post.title.like(search)).paginate(page=page, per_page=5)
    return posts

