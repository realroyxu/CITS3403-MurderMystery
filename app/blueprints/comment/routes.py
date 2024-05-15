from . import comment_bp
from . import comment_helper
from db.db_error_helper import DB_Error
from flask import request, jsonify, session


@comment_bp.route('/api/addcomment', methods=['POST'])
# need [postid, commenttext]
# [userid] will be taken from session
def add_comment():
    data = request.get_json()
    data['userid'] = session['userid']
    try:
        comment_helper.add_comment(data)
        return jsonify({"message": "Comment added successfully"}), 200
    except DB_Error as e:
        return jsonify({"message": f"Error adding comment: {e}"}), 401


@comment_bp.route('/api/editcomment', methods=['POST'])
# optional [commenttext]
# need [commentid]
def edit_comment():
    data = request.get_json()
    try:
        comment_helper.edit_comment(data)
        return jsonify({"message": "Comment edited successfully"}), 200
    except DB_Error as e:
        return jsonify({"message": f"Error editing comment: {e}"}), 401


@comment_bp.route('/api/deletecomment', methods=['POST'])
# need [commentid]
def delete_comment():
    data = request.get_json()
    try:
        comment_helper.delete_comment(data)
        return jsonify({"message": "Comment deleted successfully"}), 200
    except DB_Error as e:
        return jsonify({"message": f"Error deleting comment: {e}"}), 401
