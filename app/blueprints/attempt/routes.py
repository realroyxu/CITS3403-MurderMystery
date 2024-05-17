from . import attempt_bp
from . import attempt_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session


@attempt_bp.route('/api/getattempt', methods=['POST'])
# need [postid]
# [userid] will be taken from session
def get_attempt():
    data = request.get_json()
    try:
        data['userid'] = session['userid']
        attempt = attempt_helper.get_attempt(data)
        return jsonify({"attempt": attempt}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting attempt: {e}"}), 401


@attempt_bp.route('/api/addattempt', methods=['POST'])
# optional [progressdata]
# need [puzzleid, timeelapsed]
def add_attempt():
    data = request.get_json()
    data['userid'] = session['userid']
    try:
        attempt_helper.add_attempt(data)
        return jsonify({"message": "Attempt added successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding attempt: {e}"}), 401


@attempt_bp.route('/api/updateattempt', methods=['POST'])
# optional [progressdata]
# need [attemptid, timeelapsed]
def update_attempt():
    data = request.get_json()
    try:
        data['userid'] = session['userid']
        attempt_helper.update_attempt(data)
        return jsonify({"message": "Attempt updated successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error updating attempt: {e}"}), 401
