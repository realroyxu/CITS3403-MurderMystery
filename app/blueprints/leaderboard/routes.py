from flask import request, jsonify, session, render_template, url_for
from . import siteleaderboard_bp
import db.db_error_helper as ERROR


@siteleaderboard_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    css_file_path = url_for('static', filename='leaderboard_style.css')
    return render_template('leaderboard.html', css_file_path=css_file_path)
