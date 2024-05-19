
from . import comment_bp
from . import comment_helper
from db.db_error_helper import DB_Error
from flask import request, jsonify, session


@comment_bp.route('/api/comment/<int:id>', methods=['POST'])
def add_comment(id):
    data = request.get_json()
    if 'csrf_token' in data:
        del data['csrf_token']
    data['userid'] = session['userid']
    data['postid'] = id
    try:
        comment_helper.add_comment(data)
        return jsonify({"message": "Comment added successfully"}), 200
    except DB_Error as e:
        return jsonify({"message": f"Error adding comment: {e}"}), 401


@comment_bp.route('/api/getcomment/<int:id>', methods=['POST'])
def get_comment(id):
    try:
        comment_helper.get_comments({'postid': id})
        return jsonify({"message": "Comment get successfully"}), 200
    except DB_Error as e:
        return jsonify({"message": f"Error getting comment: {e}"}), 401
