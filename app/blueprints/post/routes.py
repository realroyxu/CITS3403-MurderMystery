from . import post_bp
from . import post_helper
from . import forms
from db import db_error_helper as ERROR
from flask import request, jsonify, session, render_template, url_for
from . import post_helper
import db.db_error_helper as ERROR
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user import user_helper

@post_bp.route('/forum/<int:id>')
def forum(id):
    form = forms.CommentForm()
    post = {
        'id': 1,
        'title': 'I solved it in 0.001s!',
        'content': 'This was a very challenging sudoku but I solved it....',
        'comments': [
            {'author': 'User1', 'text': 'Great post!'},
            {'author': 'User2', 'text': 'Thanks for sharing!'},
            {'author': 'User3', 'text': 'Interesting read.'}
        ]
    }

    if id == post['id']:
        css_file_path = url_for('static', filename='forum/forum_post_style.css')
        return render_template('forum_post.html', css_file_path=css_file_path, post=post, form=form)
    else:
        last_url = request.referrer
        css_file_path = url_for('static', filename='error/error_style.css')
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found", last_url=last_url)


@post_bp.route('/solve/<int:postid>', methods=['GET', 'POST'])
def solve(postid):
    return "Hello world"
