from . import failure_bp, failure_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session


@failure_bp.route('/api/isfailure', methods=['POST'])
# need [userid, postid]
def is_failure():
    data = request.get_json()
    try:
        result = failure_helper.is_failure(data)
        return jsonify({"result": result}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error checking failure: {e}"}), 401
