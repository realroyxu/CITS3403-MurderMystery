# this file need to be renames as api.py
from . import post_bp
from flask import request, jsonify, session, render_template, url_for
from . import post_helper
from .forms import CommentForm, GuessForm
import db.db_error_helper as ERROR
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import user_service


# very temporate solution, not using api so need duplicate function here
@post_bp.route('/forum/<int:postid>')
def forum(postid):
    try:
        comment_form = CommentForm()
        guess_form = GuessForm()
        postdata = post_helper.get_post_full(postid)
        # print(postdata)
        css_file_path = url_for('static', filename='forum/forum_post_style.css')
        return render_template('forum_post.html', css_file_path=css_file_path, post=postdata, commentform=comment_form,
                               guessform=guess_form)
    except ERROR.DB_Error:
        last_url = request.referrer
        css_file_path = url_for('static', filename='error/error_style.css')
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found",
                               last_url=last_url)


@post_bp.route('/solve/<int:id>', methods=['GET', 'POST'])
def solve(id):
    return "Hello world"
