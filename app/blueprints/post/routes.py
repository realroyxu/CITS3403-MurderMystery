from . import post_bp
from . import post_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper


@post_bp.route('/api/getpost', methods=['POST'])
# need [postid]
def get_post():
    data = request.get_json()
    try:
        post = post_helper.get_post(data)
        puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})
        comment = comment_helper.get_comments({"postid": data['postid']})
        return jsonify({"post": post, "puzzledata": puzzledata, "comment": comment}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting post: {e}"}), 401


@post_bp.route('/api/addpost', methods=['POST'])
# optional [title, content, posttype]
# need [puzzleid]
# [userid] will be taken from session, non-authorized reading is still an issue
def add_post():
    data = request.get_json()
    data['userid'] = session['userid']
    try:
        post_helper.add_post(data)
        return jsonify({"message": "Post added successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding post: {e}"}), 401


@post_bp.route('/api/editpost', methods=['POST'])
# need [postid]
# optional [title, content, posttype]
def edit_post():
    data = request.get_json()
    try:
        post_helper.edit_post(data)
        return jsonify({"message": "Post edited successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error editing post: {e}"}), 401


@post_bp.route('/api/deletepost', methods=['POST'])
# need [postid]
def delete_post():
    data = request.get_json()
    try:
        post_helper.delete_post(data)
        return jsonify({"message": "Post deleted successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error deleting post: {e}"}), 401
