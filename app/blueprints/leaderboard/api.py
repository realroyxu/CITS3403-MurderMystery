from . import siteleaderboard_bp
from . import postleaderboard_bp
from . import siteleaderboard_helper as slb_helper
from . import postleaderboard_helper as plb_helper
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


@postleaderboard_bp.route('/api/getplb', methods=['POST'])
def get_postleaderboard():
    # need [postid]
    data = request.get_json()
    try:
        return jsonify(plb_helper.get_plb(data)), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting postleaderboard: {e}"}), 401


# ISSUE: THIS IS A PUBLIC API AND THUS CAN BE EXPLOITED, NEED EXTRA VALIDATION OF PUZZLE SOLVING
@postleaderboard_bp.route('/api/addplb', methods=['POST'])
def add_postleaderboard():
    # need [postid]
    # [userid] will be taken from session
    data = request.get_json()
    try:
        data['userid'] = session['userid']
        plb_helper.add_record(data)
        return jsonify({"message": "Postleaderboard added successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding postleaderboard: {e}"}), 401
