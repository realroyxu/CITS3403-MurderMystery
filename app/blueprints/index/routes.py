from flask import render_template, flash, redirect, session, request, url_for
from . import index_bp
from app.blueprints.post import post_helper

user_scores = [
    {"username": "user1", "score": 100},
    {"username": "user2", "score": 200},
    {"username": "user3", "score": 150},
    {"username": "user4", "score": 180},
    {"username": "user5", "score": 120},
]

forum_posts = []
try:
    for i in range(1, 4):
        forum_posts.append(post_helper.get_post_full(i))
except Exception as e:
    render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    pass



@index_bp.route('/', methods=['GET'])
@index_bp.route('/index', methods=['GET'])
def index():
    css_file_path = url_for('static', filename='index_style.css')
    return render_template('index.html', css_file_path=css_file_path, forum_posts=forum_posts)


@index_bp.route('/createPost', methods=['GET'])
def createPost():
    css_file_path = url_for('static', filename='createPost_style.css')
    return render_template('createPost.html', css_file_path=css_file_path)


