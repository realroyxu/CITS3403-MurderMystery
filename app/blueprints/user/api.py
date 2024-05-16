# this is the routes file after shifting to Restful API

from . import user_api_bp
from .user_helper import user_service
from db import db_error_helper as ERROR
from flask import redirect, session, request, current_app, jsonify
from werkzeug.utils import secure_filename
import os


def allowed_file(filename, ALLOWED_EXTENSIONS=['jpg', 'jpeg', 'png', 'gif']):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        if user_service.authenticate_user(username, password):
            session['username'] = username
            session['userid'] = user_service.get_userid(username)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Login Unsuccessful. Please check username and password"}), 401
    except ERROR.DB_Error as e:
        return jsonify({"message": "Login Unsuccessful.", "DB_Error": f"{e}"}), 401


# @user_api_bp.route('/api/logout', methods=['GET'])
# def logout():
#     session.clear()
#     return jsonify({"message": "Logout successful"}), 200


@user_api_bp.route('/api/register', methods=['POST'])
# need [username, password, email]
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        user_service.register_user(username, password)
        session['username'] = username
        session['userid'] = user_service.get_userid(username)
        return jsonify({"message": f"Account created for {username}!"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error creating account: {e}"}), 401


@user_api_bp.route('/api/changepassword', methods=['POST'])
# need [old_password, new_password]
def change_password():
    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']
    try:
        user_service.change_password(session['userid'], old_password, new_password)
        return jsonify({"message": "Password changed successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error changing password: {e}"}), 401


# redirect will be done by javascript, however, session will still be cleared by backend
# session.clear() won't work since clearing session will interrupt the function, considering using AJAX
# but leave it here and use client-side redirect for now

@user_api_bp.route('/api/changeavatar', methods=['POST'])
def upload_avator():
    # similar to official sample
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 401
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 401
    if file and allowed_file(file.filename):
        filename = str(session['username']) + os.path.splitext(secure_filename(file.filename))[1]
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        try:
            user_service.change_avatar(session['userid'], filename)
        except ERROR.DB_Error as e:
            return jsonify({"message": f"Error changing avatar: {e}"}), 401
        return jsonify({"message": "Avatar changed successfully"}), 200


