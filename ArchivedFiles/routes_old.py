# from app import app
# from flask import render_template, flash, redirect, session, request
# import app.blueprints.user.user_helper as User
# import db.db_error_helper as ERROR
# from werkzeug.utils import secure_filename
# import os
#
# user_scores = [
#     {"username": "user1", "score": 100},
#     {"username": "user2", "score": 200},
#     {"username": "user3", "score": 150},
#     {"username": "user4", "score": 180},
#     {"username": "user5", "score": 120},
# ]
#
# forum_posts = [
#     {"id": 1, "title": "Post 1",
#      "content": "This is the content of post 1. This is the content of post 1.This is the content of post 1. This is the content of post 1. This is the content of post 1. v v v This is the content of post 1. This is the content of post 1. v "},
#     {"id": 2, "title": "Post 2", "content": "This is the content of post 2."},
#     {"id": 3, "title": "Post 3", "content": "This is the content of post 3."},
#     {"id": 4, "title": "Post 4", "content": "This is the content of post 4."},
#     {"id": 5, "title": "Post 5", "content": "This is the content of post 5."},
# ]
#
#
# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('/pages/index.html', css_file_path='/static/index_style.css',
#                            sample_data=leaderboard.sort_data(user_scores), forum_posts=forum_posts)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = forms.LoginForm()
#     if form.validate_on_submit():
#         try:
#             if User.authenticate_user(form.username.data, form.password.data):
#                 session['username'] = form.username.data
#                 session['userid'] = User.get_userid(form.username.data)
#                 return redirect('/index')
#         except ERROR.DB_Error as e:
#             return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
#     return render_template('/pages/login.html', css_file_path="/static/login_style.css", form=form)
#
#
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/index')
#
#
# @app.route('/userhome')
# def user_home():
#     return render_template('/pages/userhome.html', css_file_path="/static/userhome_style.css")
#
#
# def allowed_file(filename, ALLOWED_EXTENSIONS=['jpg', 'jpeg', 'png', 'gif']):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @app.route('/changeavatar', methods=['GET', 'POST'])
# def upload_avator():
#     # similar to official sample
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = session['userid'] + os.path.splitext(secure_filename(file.filename))[1]
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             try:
#                 User.change_avatar(session['userid'], filename)
#             except ERROR.DB_Error as e:
#                 return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
#             render_template('/pages/changeavatar.html', css_file_path="/static/changeavatar_style.css")
#     return render_template('/pages/changeavatar.html', css_file_path="/static/changeavatar_style.css")
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = forms.RegistrationForm()
#     if form.validate_on_submit():
#         try:
#             User.register_user(form.username.data, form.password.data, form.email.data)
#             session['username'] = form.username.data
#             session['userid'] = User.get_userid(form.username.data)
#             flash(f"Account created for {form.username.data}!", 'success')
#             return redirect('/index')
#         except ERROR.DB_Error as e:
#             return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
#     return render_template('/pages/register.html', css_file_path="/static/register_style.css", form=form)
#
#
# @app.route('/changepassword', methods=['GET', 'POST'])
# def change_password():
#     form = forms.ChangePasswordForm()
#     if form.validate_on_submit():
#         try:
#             User.change_password(session['userid'], form.old_password.data, form.new_password.data)
#             flash(f"Password changed for {session['username']}!", 'success')
#             # redirect will be done by javascript, however, session will still be cleared by backend
#             # session.clear()
#             # this won't work since clearing session will interrupt the function, considering using AJAX
#             # but leave it here and use client-side redirect for now
#             return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css", form=form)
#         except ERROR.DB_Error as e:
#             flash(f"Error changing password: {e}", 'error')
#             return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css", form=form)
#     return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css", form=form)
#
#
# @app.route('/leaderboard')
# def leaderboard():
#     data = leaderboard.sort_data(user_scores)
#     return render_template('/pages/leaderboard.html', css_file_path="/static/leaderboard_style.css", sample_data=data)
#
#
# @app.route('/forum/{id}')
# def forum(id):
#     return
#
#
# @app.route('/createSudoku')
# def createSudoku():
#     return render_template('/pages/createSudoku.html')
