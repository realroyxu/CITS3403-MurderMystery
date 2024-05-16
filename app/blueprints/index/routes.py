from flask import render_template, flash, redirect, session, request, url_for
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

@index_bp.route('/', methods=['GET'])
@index_bp.route('/index', methods=['GET'])
def index():
    css_file_path = url_for('static', filename='index_style.css')
    return render_template('index.html', css_file_path=css_file_path)


@index_bp.route('/createSudoku', methods=['GET'])
def createSudoku():
    return render_template('createSudoku.html')

@index_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    return render_template('leaderboard.html')
