import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session


def comment_fieldcheck(data):
    valid_field = ['userid', 'commenttext', 'commenttime', 'postid']
    if not all(field in valid_field for field in data.keys()):
        raise RuntimeError("Error adding comment: invalid field provided.")
    return


def get_comment(Comment, data):
    if 'commentid' not in data:
        raise RuntimeError("Error fetching comment: commentid not provided.")
    with Session() as s:
        try:
            stmt = select(Comment).where(Comment.commentid == data['commentid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching comment: No comment found.")


def add_comment(Comment, data):
    if 'userid' not in data:
        raise RuntimeError("Error adding comment: userid not provided.")
    if 'commenttime' not in data:
        raise RuntimeError("Error adding comment: commenttime not provided.")
    with Session() as s:
        try:
            comment_fieldcheck(data)
            comment = Comment(**data)
            s.add(comment)
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error adding comment: {e}") from e
    return "Comment added successfully."


def edit_comment(Comment, data):
    if 'commentid' not in data:
        raise RuntimeError("Error editing comment: commentid not provided.")
    if 'commenttime' not in data:
        raise RuntimeError("Error editing comment: commenttime not provided.")
    with Session() as s:
        try:
            stmt = select(Comment).where(Comment.commentid == data['commentid'])
            origin = s.execute(stmt).scalar_one()
            origin.commenttext = data.get('commenttext', origin.commenttext)
            origin.commenttime = data.get('commenttime', origin.commenttime)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error editing comment: No comment found.")
        return "Comment updated successfully."


def delete_comment(Comment, data):
    if 'commentid' not in data:
        raise RuntimeError("Error deleting comment: commentid not provided.")
    with Session() as s:
        try:
            stmt = select(Comment).where(Comment.commentid == data['commentid'])
            s.execute(stmt)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error deleting comment: No comment found.")
        return "Comment deleted successfully."
