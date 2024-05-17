import sqlalchemy.exc
from sqlalchemy import *
from db.database import Session
import db.db_error_helper as ERROR


def comment_fieldcheck(data):
    valid_field = ['userid', 'commenttext', 'commenttime', 'postid']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("invalid field provided.")
    return


# this function is not called in comment helper, but from post helper
def get_comments(Comment, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    with Session() as s:
        try:
            stmt = select(Comment.userid, Comment.commenttext, Comment.commenttime).where(
                Comment.postid == data['postid'])
            res = s.execute(stmt).all()
            if res:
                # need to lookup this mapping method but it works anyway
                return [dict(row._mapping) for row in res]
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No comment found.")


def add_comment(Comment, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'commenttime' not in data:
        raise ERROR.DB_Error("commenttime not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    with Session() as s:
        try:
            comment_fieldcheck(data)
            comment = Comment(**data)
            s.add(comment)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e


def edit_comment(Comment, data):
    if 'commentid' not in data:
        raise ERROR.DB_Error("commentid not provided.")
    if 'commenttime' not in data:
        raise ERROR.DB_Error("commenttime not provided.")
    with Session() as s:
        try:
            stmt = select(Comment).where(Comment.commentid == data['commentid'])
            origin = s.execute(stmt).scalar_one()
            origin.commenttext = data.get('commenttext', origin.commenttext)
            origin.commenttime = data.get('commenttime', origin.commenttime)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No comment found.")


def delete_comment(Comment, data):
    if 'commentid' not in data:
        raise ERROR.DB_Error("commentid not provided.")
    with Session() as s:
        try:
            stmt = delete(Comment).where(Comment.commentid == data['commentid'])
            s.execute(stmt)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No comment found.")
