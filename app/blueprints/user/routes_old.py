# this is the old version of routes.py, depending heavily on Jinja
from . import user_bp
from . import user_helper
from . import forms_old
from db import db_error_helper as ERROR
from flask import render_template, flash, redirect, session, request, current_app
from werkzeug.utils import secure_filename
import os


def allowed_file(filename, ALLOWED_EXTENSIONS=['jpg', 'jpeg', 'png', 'gif']):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            if user_helper.authenticate_user(form.username.data, form.password.data):
                session['username'] = form.username.data
                session['userid'] = user_helper.get_userid(form.username.data)
                return redirect('/index')
            else:
                flash("Login Unsuccessful. Please check username and password", 'error')
                return redirect('/login')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/login.html', css_file_path="/static/login_style.css", form=form)


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/index')


@user_bp.route('/userhome')
def user_home():
    return render_template('/pages/userhome.html', css_file_path="/static/userhome_style.css")


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            user_helper.register_user(form.username.data, form.password.data, form.email.data)
            session['username'] = form.username.data
            session['userid'] = user_helper.get_userid(form.username.data)
            flash(f"Account created for {form.username.data}!", 'success')
            return redirect('/index')
        except ERROR.DB_Error as e:
            return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
    return render_template('/pages/register.html', css_file_path="/static/register_style.css", form=form)


@user_bp.route('/changepassword', methods=['GET', 'POST'])
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        try:
            user_helper.change_password(session['userid'], form.old_password.data, form.new_password.data)
            flash(f"Password changed for {session['username']}!", 'success')
            # redirect will be done by javascript, however, session will still be cleared by backend
            # session.clear()
            # this won't work since clearing session will interrupt the function, considering using AJAX
            # but leave it here and use client-side redirect for now
            return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css",
                                   form=form)
        except ERROR.DB_Error as e:
            flash(f"Error changing password: {e}", 'error')
            return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css",
                                   form=form)
    return render_template('/pages/changepassword.html', css_file_path="/static/changepassword_style.css", form=form)


@user_bp.route('/changeavatar', methods=['GET', 'POST'])
def upload_avator():
    # similar to official sample
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(session['username']) + os.path.splitext(secure_filename(file.filename))[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            try:
                user_helper.change_avatar(session['userid'], filename)
            except ERROR.DB_Error as e:
                return render_template('/error/error.html', css_file_path="/static/error/error_style.css", error=e)
            flash("Avatar changed successfully", 'success')
            render_template('/pages/changeavatar.html', css_file_path="/static/changeavatar_style.css")
        else:
            flash('Invalid file type')
            return redirect(request.url)
    return render_template('/pages/changeavatar.html', css_file_path="/static/changeavatar_style.css")
