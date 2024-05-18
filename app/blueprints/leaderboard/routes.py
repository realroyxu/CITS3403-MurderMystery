from . import postleaderboard_bp as plb_bp
from flask import request, jsonify, session, render_template, url_for
from . import postleaderboard_helper as plb_helper
import db.db_error_helper as ERROR


@plb_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    css_file_path = url_for('static', filename='leaderboard_style.css')
    return render_template('leaderboard.html', css_file_path=css_file_path)
