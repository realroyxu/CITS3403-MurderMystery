from . import puzzle_bp
from . import puzzle_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session, current_app


@puzzle_bp.route('/api/getpuzzle', methods=['POST'])
# need [puzzleid]
def get_puzzle():
    data = request.get_json()
    try:
        puzzle = puzzle_helper.get_puzzle(data)
        return jsonify({"puzzle": puzzle}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting puzzle: {e}"}), 401


@puzzle_bp.route('/api/addpuzzle', methods=['POST'])
# optional [category]
# need [puzzledata]
def add_puzzle():
    data = request.get_json()
    data['userid'] = session['userid']
    try:
        puzzle_helper.add_puzzle(data)
        return jsonify({"message": "Puzzle added successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding puzzle: {e}"}), 401


@puzzle_bp.route('/api/editpuzzle', methods=['POST'])
# optional [category, puzzledata]
def edit_puzzle():
    data = request.get_json()
    try:
        puzzle_helper.edit_puzzle(data)
        return jsonify({"message": "Puzzle edited successfully"}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error editing puzzle: {e}"}), 401


@puzzle_bp.route('/api/verifyanswer', methods=['POST'])
# another api exposure problem, leave it here for now
# need [puzzleid, puzzleanswer]
def verify_answer():
    data = request.get_json()
    try:
        result = puzzle_helper.verify_answer(data)
        return jsonify({"result": result}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error verifying answer: {e}"}), 401
