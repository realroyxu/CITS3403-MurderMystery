from . import siteleaderboard_bp
from . import siteleaderboard_helper as slb_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session
from app.blueprints.user.user_helper import user_service


@siteleaderboard_bp.route('/api/getslbbypost', methods=['GET'])
def get_siteleaderboard_postcount_order():
    try:
        limit = int(request.args.get('limit', 10))
        data = slb_helper.get_slb_by_post(limit)
        for item in data:
            item['username'] = user_service.get_username(item['userid'])
            item.pop('userid')
        return jsonify(data), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting siteleaderboard: {e}"}), 401

@siteleaderboard_bp.route('/api/getslbbysolve', methods=['GET'])
def get_siteleaderboard_solvecount_order():
    try:
        limit = int(request.args.get('limit', 10))
        data = slb_helper.get_slb_by_solve(limit)
        for item in data:
            item['username'] = user_service.get_username(item['userid'])
            item.pop('userid')
        return jsonify(data), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting siteleaderboard: {e}"}), 401
