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
        css_file_path = url_for('static', filename='forum/forum_post_style.css')
        return render_template('forum_post.html', css_file_path=css_file_path, post=postdata, commentform=comment_form,
                               guessform=guess_form)
    except ERROR.DB_Error:
        last_url = request.referrer
        css_file_path = url_for('static', filename='error/error_style.css')
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found",
                               last_url=last_url)

@post_bp.route('/forums')
def forums():
    overlimit = False
    index = request.args.get('start', default=0, type=int)
    limit = 5
    next_start = index + limit
    previous_start = max(index - limit, 0)
    try:
        postdata = post_helper.get_all_posts_with_comments(index, limit)
        if len(postdata) < limit:
            overlimit = True
        css_file_path = url_for('static', filename='forums_style.css')
        return render_template('forums.html', css_file_path=css_file_path, postdata=postdata, next_start=next_start, previous_start=previous_start, overlimit=overlimit)
    except ERROR.DB_Error:
        last_url = request.referrer
        css_file_path = url_for('static', filename='error/error_style.css')
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found", last_url=last_url)
