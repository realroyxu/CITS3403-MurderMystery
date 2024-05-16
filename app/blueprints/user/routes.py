from . import user_bp, forms_old as forms
from flask import render_template, url_for, flash, session
import requests


@user_bp.route('/login', methods=['GET'])
def login_page():
    form = forms.LoginForm()
    return render_template('login.html', form=form)


@user_bp.route('/userhome')
def user_home():
    return render_template('userhome.html', css_file_path="/static/userhome_style.css")


@user_bp.route('/register', methods=['GET'])
def register_page():
    form = forms.RegistrationForm()
    return render_template('register.html', form=form)


@user_bp.route('/changepassword', methods=['GET'])
def change_password_page():
    form = forms.ChangePasswordForm()
    return render_template('changepassword.html', form=form)


@user_bp.route('/changeavatar', methods=['GET'])
def change_avatar_page():
    return render_template('changeavatar.html')


@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash("Logout successful", 'success')
    return render_template('index.html', css_file_path='/static/index_style.css')
