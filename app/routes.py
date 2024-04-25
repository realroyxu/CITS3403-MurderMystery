from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('/pages/index.html')

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
