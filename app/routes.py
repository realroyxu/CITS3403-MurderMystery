from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('/pages/index.html')

@app.route('/login')
def login():
    return

@app.route('/register')
def register():
    return

@app.route('/leaderboard')
def leaderboard():
    return

@app.route('/forum/{id}')
def forum(id):
    return


@app.route('/createForum/{id}')
def createSudoku(id):
    return
