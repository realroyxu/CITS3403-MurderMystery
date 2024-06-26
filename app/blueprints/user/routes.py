from . import forms, user_bp
from flask import render_template, url_for, flash, session

@user_bp.route('/user/login')
def login_page():
    css_file_path = url_for('static', filename='login_style.css')
    form = forms.LoginForm()
    return render_template('login.html', form=form, css_file_path=css_file_path)


@user_bp.route('/user/home')
def user_home():
    css_file_path = url_for('static', filename='userhome_style.css')
    return render_template('userhome.html', css_file_path=css_file_path)


@user_bp.route('/user/register', methods=['GET'])
def register_page():
    css_file_path = url_for('static', filename='register_style.css')
    form = forms.RegistrationForm()
    return render_template('register.html', form=form, css_file_path=css_file_path)


@user_bp.route('/user/changepassword', methods=['GET'])
def change_password_page():
    css_file_path = url_for('static', filename='change_password_style.css')
    form = forms.ChangePasswordForm()
    return render_template('change_password.html', form=form, css_file_path=css_file_path)


@user_bp.route('/user/changeavatar', methods=['GET'])
def change_avatar_page():
    return render_template('changeavatar.html')


@user_bp.route('/user/logout', methods=['GET'])
def logout():
    session.clear()
    flash("Logout successful", 'success')
    return render_template('index.html', css_file_path='/static/index_style.css')
