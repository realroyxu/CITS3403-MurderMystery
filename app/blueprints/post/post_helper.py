import app.blueprints.post.post_db_helper as Post_DB
import db.db_error_helper as ERROR
from app.models.post import Post
from datetime import datetime


def add_post(userid, title, content, posttype, puzzleid):
    """Add new post"""
    posttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "userid": userid,
        "title": title,
        "content": content,
        "posttime": posttime,
        "posttype": posttype,
        "puzzleid": puzzleid
    }
    try:
        return Post_DB.add_post(Post, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))

