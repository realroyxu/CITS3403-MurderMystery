# this is the routes file after shifting to Restful API

from . import user_api_bp
from .user_helper import user_service
from db import db_error_helper as ERROR
from flask import session, request, jsonify
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

@user_api_bp.route('/api/register', methods=['POST'])
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
def change_password():
    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']
    print(session['userid'])
    try:
        user_service.change_password(session['userid'], old_password, new_password)
        return jsonify({"message": "Password changed successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error changing password: {e}"}), 401

@user_api_bp.route('/api/changeavatar', methods=['POST'])
def change_avatar():
    data = request.get_json()
    avatar_id = data['avatar_id']
    user_id = session['userid']

    if not avatar_id or not user_id:
        return jsonify({"message": "Invalid request"}), 400

    try:
        user_service.change_avatar(user_id, avatar_id)
        return jsonify({"message": "Avatar changed successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error changing avatar: {e}"}), 500


