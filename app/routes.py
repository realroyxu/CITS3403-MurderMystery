from app import app
from flask import render_template, flash, redirect, session, request
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
        {
            'id': 1,
            'title': 'I solved it in 0.001s!',
            'content': 'This was a very challenging sudoku but I solved it....',
            'image_url': '../../static/images/sudoku.png',
            'comments': [
                {'author': 'User1', 'text': 'Great post!'},
                {'author': 'User2', 'text': 'Thanks for sharing!'},
                {'author': 'User3', 'text': 'Interesting read.'}
            ]
        },
        {
            'id': 2,
            'title': 'CITS3403 is uh',
            'content': 'CITS3403 is so fun!!!!! just kidding....',
            'image_url': '../../static/images/sudoku.png',
            'comments': [
                {'author': 'User4', 'text': 'I love Sudoku!'},
                {'author': 'User5', 'text': 'Can you share more tips?'}
            ]
        }
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
            last_url = request.referrer
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e, last_url=last_url)
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
            User.register_user(form.username.data, form.password.data)
            session['username'] = form.username.data
            flash(f"Account created for {form.username.data}!", 'success')
            return redirect('/index')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/register.html', css_file_path="/static/register_style.css", form=form)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return None

@app.route('/leaderboard')
def leaderboard():
    data = Leaderboard.sort_data(user_scores)
    return render_template('/pages/leaderboard.html', css_file_path="/static/leaderboard_style.css", sample_data=data)

@app.route('/forum/<int:id>')
def forum(id):
    post = {
        'id': 1,
        'title': 'I solved it in 0.001s!',
        'content': 'This was a very challenging sudoku but I solved it....',
        'comments': [
            {'author': 'User1', 'text': 'Great post!'},
            {'author': 'User2', 'text': 'Thanks for sharing!'},
            {'author': 'User3', 'text': 'Interesting read.'}
        ]
    }

    if id == post['id']:
        return render_template('pages/forum_post.html', css_file_path='/static/forum/forum_post_style.css', post=post)
    else:
        last_url = request.referrer
        return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error="Post not found", last_url=last_url)


@app.route('/solve/<int:id>', methods=['GET', 'POST'])
def solve(id):
    return

@app.route('/createSudoku')
def createSudoku():
    return render_template('/pages/createSudoku.html')
