from app import app
from flask import render_template, flash, redirect, session, jsonify
import app.user.user_helper as User
import app.user.forms as Forms
import app.leaderboard.leaderboard as Leaderboard
import db.db_error_helper as ERROR

user_scores = [
    {"username": "user1", "score": 100},
    {"username": "user2", "score": 200},
    {"username": "user3", "score": 150},
    {"username": "user4", "score": 180},
    {"username": "user5", "score": 120},
]

forum_posts = [
    {"id": 1, "title": "Post 1", "content": "This is the content of post 1. This is the content of post 1.This is the content of post 1. This is the content of post 1. This is the content of post 1. v v v This is the content of post 1. This is the content of post 1. v "},
    {"id": 2, "title": "Post 2", "content": "This is the content of post 2."},
    {"id": 3, "title": "Post 3", "content": "This is the content of post 3."},
    {"id": 4, "title": "Post 4", "content": "This is the content of post 4."},
    {"id": 5, "title": "Post 5", "content": "This is the content of post 5."},
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('/pages/index.html', css_file_path='/static/index_style.css', sample_data=Leaderboard.sort_data(user_scores), forum_posts=forum_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Forms.LoginForm()
    if form.validate_on_submit():
        try:
            if User.authenticate_user(form.username.data, form.password.data):
                session['username'] = form.username.data
                return redirect('/index')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/login.html', css_file_path="/static/login_style.css", form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            User.register_user(form.username.data, form.password.data, form.email.data)
            session['username'] = form.username.data
            flash(f"Account created for {form.username.data}!", 'success')
            return redirect('/index')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/register.html', css_file_path="/static/register_style.css", form=form)

@app.route('/changepassword', methods=['GET', 'POST'])
def change_password():
    form = Forms.ChangePasswordForm()
    if form.validate_on_submit():
        try:
            User.change_password(session['username'], form.old_password.data, form.new_password.data)
            flash(f"Password changed for {session['username']}!", 'success')
            # logout and redirect to login
            logout()
            return redirect('/login')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css", form=form)

@app.route('/leaderboard')
def leaderboard():
    data = Leaderboard.sort_data(user_scores)
    return render_template('/pages/leaderboard.html', css_file_path="/static/leaderboard_style.css", sample_data=data)

@app.route('/forum/{id}')
def forum(id):
    return


@app.route('/createSudoku')
def createSudoku():
    return render_template('/pages/createSudoku.html')
