from . import comment_db_helper as Comment_DB
import db.db_error_helper as ERROR
from app.models.comment import Comment
from datetime import datetime


def get_comments(data):
    """Get all comment for 1 post by postid"""
    try:
        return Comment_DB.get_comments(Comment, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_comment(data):
    """Add new comment"""
    data['commenttime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Comment_DB.add_comment(Comment, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def edit_comment(data):
    """Edit comment"""
    data['commenttime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Comment_DB.edit_comment(Comment, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
