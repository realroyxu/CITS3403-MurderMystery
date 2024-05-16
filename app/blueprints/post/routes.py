from . import post_bp
from . import post_helper
from db import db_error_helper as ERROR
from flask import request, jsonify, session, render_template, url_for

@post_bp.route('/forum/<int:id>')
def forum(id):
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
        return render_template('forum_post.html', css_file_path=css_file_path, post=post)
    else:
        last_url = request.referrer
        css_file_path = url_for('static', filename='error/error_style.css')
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found", last_url=last_url)

@post_bp.route('/solve/<int:id>', methods=['GET', 'POST'])
def solve(id):
    return "Hello world"
