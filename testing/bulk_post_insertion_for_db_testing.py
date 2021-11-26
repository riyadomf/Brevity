"""
Automated Insertion of bulk posts from json for testing pagination feature.
Warning: There should be at least 2 registered user as the json data contains 2 user. 
"""
import sys, os, json
sys.path.append('../brevity')
from brevity import db
from brevity.models import Post, load_user


"""
scrape data from url
"""
# import requests
# def scrape_json(url):
#     posts = requests.get(url, headers = { "Accept" : "application/json" }).json()
#     return posts

"""
read data from file
"""
def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


"""
insert post in database
"""
def insert_bulk_post(posts):
    for p in posts:
        post = Post(title = p.get("title"), content = p.get("content"), author = load_user(p.get("user_id")))
        db.session.add(post)
    db.session.commit()


posts = read_file(os.path.join('testing', "bulk_post_insertion_for_db_testing.json"))
insert_bulk_post(posts)
