from . import post_db_helper as Post_DB
import db.db_error_helper as ERROR
from app.models.post import Post
from datetime import datetime
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import UserService

user_helper = UserService()


def get_post(data):
    """Get post data by postid"""
    try:
        return Post_DB.get_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_post(data):
    """Add new post"""
    new_post = {
        'userid': data['userid'],
        'title': data.get('title', '(NO TITLE)'),
        'content': data.get('content', '(NO CONTENT)'),
        'posttime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'posttype': data.get('posttype', '(Unknown)'),
        'puzzleid': data.get('puzzleid', 1)
    }

    try:
        return Post_DB.add_post(Post, new_post)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def edit_post(data):
    """Edit post"""
    data['posttime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Post_DB.edit_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def delete_post(data):
    """Delete post"""
    try:
        return Post_DB.delete_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_post_full(postid):
    post = get_post({'postid': postid})
    print(post)
    # we don't want everyone knows the puzzle answer :P
    puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})['puzzledata']
    print(puzzledata)
    comment = comment_helper.get_comments({"postid": postid})
    if comment:
        for item in comment:
            item['author'] = user_helper.get_username(item['userid'])
            item['avatarid'] = user_helper.get_avatarid(item['userid'])
    return {"postid": post['postid'], "title": post['title'], "content": post['content'],
            "puzzledata": puzzledata, "comments": comment, "postimage": post['postimage']}


def add_image(data):
    try:
        return Post_DB.add_image(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
