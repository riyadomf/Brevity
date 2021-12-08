from brevity.models import Post, Tag, Upvote
from brevity import db
from sqlalchemy import func, or_

AdmindefinedTag = {
    "dbms" : "database",
    "database" : "dbms",
    "swe" : "software engineering",
    "software engineering" : "swe",
    "artificial intelligence" : "ai",
    "ai" : "artificial intelligence",
    "data structure" : "ds",
    "ds" : "data structure",
    "competitive programming" : "cp",
    "cp" : "competitive programming",
    "bst" : "binary search tree",
    "binary search tree" : "bst",
    "breadth first search" : "bfs",
    "bfs" : "breadth first search",
    "depth first search" : "dfs",
    "dfs" : "depth first search",
    "digital signal processing" : "dsp",
    "dsp" : "digital signal processing",
    "operating system" : "os",
    "os" : "operating system",
    "machine learning" : "ml",
    "ml" : "machine learning"

}
### search type tag(tag_type=0)
### otherwise(tag_type=1)
def search_result(searched_val,page,type):
    
   
    search = "%{}%".format(searched_val)

    tag_type=1

    sz = len(searched_val)
    if searched_val[0]=='[' and searched_val[sz-1]==']':
        tag_type=0
    if searched_val[0]=='[' and tag_type==0:
        searched_val = searched_val[1:]
    sz = len(searched_val)
    if searched_val[sz-1]==']' and tag_type==0:
        searched_val = searched_val[:sz-1]

    if tag_type==0:
        searched_val = searched_val.lower()
        AdminChosenTag = searched_val
        if(searched_val in AdmindefinedTag):
            AdminChosenTag = AdmindefinedTag[searched_val]

        AdminChosenTag = AdminChosenTag.lower()

        if type==0:
            posts = db.session.query(Post).join(Tag).filter(Post.id==Tag.post_id).filter(or_(func.lower(Tag.tag)==searched_val,func.lower(Tag.tag)==AdminChosenTag)).paginate(page=page, per_page=5)
        elif type==1:
            posts = db.session.query(Post).join(Tag).filter(Post.id==Tag.post_id).filter(or_(func.lower(Tag.tag)==searched_val,func.lower(Tag.tag)==AdminChosenTag)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        else:
            posts = db.session.query(Post).join(Tag).join(Upvote).filter(Post.id==Tag.post_id).filter(Post.id==Upvote.post_id).filter(or_(func.lower(Tag.tag)==searched_val,func.lower(Tag.tag)==AdminChosenTag)).group_by(Post.id).order_by(func.count(Post.id).desc()).paginate(page=page, per_page=5)
    else:
        if type==0:
            posts = Post.query.filter(Post.title.like(search)).paginate(page=page, per_page=5)
        elif type==1:
            posts = Post.query.filter(Post.title.like(search)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        else:
            posts = db.session.query(Post).join(Upvote).filter(Post.id==Upvote.post_id).filter(Post.title.like(search)).group_by(Post.id).order_by(func.count(Post.id).desc()).paginate(page=page, per_page=5)

    
    return posts

