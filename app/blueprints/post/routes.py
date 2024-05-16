from . import post_bp
from flask import request, jsonify, session, render_template, url_for
from . import post_helper
import db.db_error_helper as ERROR
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import user_service

# very temporate solution, not using api so need duplicate function here
@post_bp.route('/forum/<int:postid>')
def forum(postid):
    try:
        post = post_helper.get_post({'postid': postid})
        puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})
        comment = comment_helper.get_comments({"postid": postid})
        for item in comment:
            item['author'] = user_service.get_username(item['userid'])
            item.pop('userid')
        print(post)
        postdata = {"postid": post['postid'], "title": post['title'], "content": post['content'],
                    "puzzledata": puzzledata, "comments": comment}
        if postid == post['postid']:
            css_file_path = url_for('static', filename='forum/forum_post_style.css')
            return render_template('forum_post.html', css_file_path=css_file_path, post=postdata)
        else:
            last_url = request.referrer
            css_file_path = url_for('static', filename='error/error_style.css')
            return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found",
                                   last_url=last_url)
    except ERROR.DB_Error:
        return render_template('/error/error.html', css_file_path=css_file_path, error="Post not found",
                               last_url=last_url)



@post_bp.route('/solve/<int:id>', methods=['GET', 'POST'])
def solve(id):
    return "Hello world"
