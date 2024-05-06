import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session


def get_post(Post, data):
    # get post data by postid
    if 'postid' not in data:
        raise RuntimeError("Error fetching post: postid not provided.")
    with Session() as s:
        try:
            stmt = select(Post).where(Post.postid == data['postid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching post: No post found.")


def add_post(Post, data):
    if 'userid' not in data:
        raise RuntimeError("Error adding post: userid not provided.")
    if 'posttime' not in data:
        raise RuntimeError("Error adding post: posttime not provided.")
    valid_field = ['userid', 'title', 'content', 'posttime', 'posttype', 'puzzleid']
    if not all(field in valid_field for field in data.keys()):
        raise RuntimeError("Error adding post: invalid field provided.")
    with Session() as s:
        try:
            post = Post(**data)
            s.add(post)
            s.commit()
        # Need to test which exception will be raised in this method, for now use generic Expection
        except Exception as e:
            raise RuntimeError(f"Error adding post: {e}") from e


def delete_post(Post, data):
    if 'postid' not in data:
        raise RuntimeError("Error deleting post: postid not provided.")
    with Session() as s:
        try:
            stmt = delete(Post).where(Post.postid == data['postid'])
            s.execute(stmt)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error deleting post: No post found.")
        except Exception as e:
            raise RuntimeError(f"Error deleting post: {e}") from e

