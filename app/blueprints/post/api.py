from . import post_api_bp
from . import post_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session, render_template, url_for, current_app
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import user_service

import os
from werkzeug.utils import secure_filename


@post_api_bp.route('/api/getpost', methods=['POST'])
# need [postid]
def get_post():
    data = request.get_json()
    try:
        post = post_helper.get_post(data)
        puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})
        comment = comment_helper.get_comments({"postid": data['postid']})
        for item in comment:
            item['author'] = user_service.get_username(item['userid'])
            item.pop('userid')
        return jsonify({"postid": post['postid'], "title": post['title'], "content": post['content'],
                        "puzzledata": puzzledata, "comments": comment}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting post: {e}"}), 401


# @post_api_bp.route('/api/addpost', methods=['POST'])
# # optional [title, content, posttype]
# # need [puzzleid]
# # [userid] will be taken from session, non-authorized reading is still an issue
# def add_post():
#     data = request.get_json()
#     data['userid'] = session['userid']
#     try:
#         post_helper.add_post(data)
#         return jsonify({"message": "Post added successfully"}), 200
#     except ERROR.DB_Error as e:
#         return jsonify({"message": f"Error adding post: {e}"}), 401

@post_api_bp.route('/api/addpost', methods=['POST'])
def add_post():
    data = request.form.to_dict()
    data['userid'] = session.get('userid')
    if not data['userid']:
        return jsonify({"message": "User not authorized"}), 401

    try:
        post_helper.add_post(data)
        return jsonify({"message": "Post added successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding post: {e}"}), 401


@post_api_bp.route('/api/editpost', methods=['POST'])
# need [postid]
# optional [title, content, posttype]
def edit_post():
    data = request.get_json()
    try:
        post_helper.edit_post(data)
        return jsonify({"message": "Post edited successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error editing post: {e}"}), 401


@post_api_bp.route('/api/deletepost', methods=['POST'])
# need [postid]
def delete_post():
    data = request.get_json()
    try:
        post_helper.delete_post(data)
        return jsonify({"message": "Post deleted successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error deleting post: {e}"}), 401


def allowed_file(filename, ALLOWED_EXT=['jpg', 'jpeg', 'png', 'gif']):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# using param in link is not very safe, well but it's easier to implement without introducing overhead & bugs
@post_api_bp.route('/api/uploadimage/<int:postid>', methods=['POST'])
def upload_image(postid):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 401
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 401
        if file and allowed_file(file.filename):
            # if there's one file with the same name (ignoring ext name), it will be overwritten
            for existing_file in os.listdir(current_app.config['UPLOAD_FOLDER']):
                existing_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], existing_file)
                if os.path.isfile(existing_file_path) and existing_file.startswith(str(postid) + '.'):
                    os.remove(existing_file_path)
            # save file
            filename = str(postid) + os.path.splitext(secure_filename(file.filename))[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": "Image uploaded successfully"}), 200
        else:
            return jsonify({"message": "Invalid file type"}), 401
