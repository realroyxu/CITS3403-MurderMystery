from app import app
from flask import render_template

user_scores = [
    {"username": "user1", "score": 100},
    {"username": "user2", "score": 200},
    {"username": "user3", "score": 150},
    {"username": "user4", "score": 180},
    {"username": "user5", "score": 120},
]

forum_posts = [
    {"id": 1, "title": "Post 1", "content": "This is the content of post 1."},
    {"id": 2, "title": "Post 2", "content": "This is the content of post 2."},
    {"id": 3, "title": "Post 3", "content": "This is the content of post 3."},
    {"id": 4, "title": "Post 4", "content": "This is the content of post 4."},
    {"id": 5, "title": "Post 5", "content": "This is the content of post 5."},
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('/pages/index.html', css_file_path='/static/index_style.css', sample_data=user_scores, forum_posts=forum_posts)

@app.route('/login')
def login():
    return render_template('/pages/login.html', css_file_path="/static/login_style.css")

@app.route('/register')
def register():
    return render_template('/pages/register.html', css_file_path="/static/register_style.css")

@app.route('/leaderboard')
def leaderboard():
    return render_template('/pages/leaderboard.html')

@app.route('/forum/{id}')
def forum(id):
    return


@app.route('/createSudoku')
def createSudoku():
    return render_template('/pages/createSudoku.html')
