from flask import render_template, flash, redirect, session, request
from . import index_bp

user_scores = [
    {"username": "user1", "score": 100},
    {"username": "user2", "score": 200},
    {"username": "user3", "score": 150},
    {"username": "user4", "score": 180},
    {"username": "user5", "score": 120},
]

forum_posts = [
    {"id": 1, "title": "Post 1",
     "content": "This is the content of post 1. This is the content of post 1.This is the content of post 1. This is the content of post 1. This is the content of post 1. v v v This is the content of post 1. This is the content of post 1. v "},
    {"id": 2, "title": "Post 2", "content": "This is the content of post 2."},
    {"id": 3, "title": "Post 3", "content": "This is the content of post 3."},
    {"id": 4, "title": "Post 4", "content": "This is the content of post 4."},
    {"id": 5, "title": "Post 5", "content": "This is the content of post 5."},
]

@index_bp.route('/')
@index_bp.route('/index')
def index():
    return render_template('/pages/index.html', css_file_path='/static/index_style.css')
