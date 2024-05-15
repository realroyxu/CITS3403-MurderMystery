import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
from app.models.siteleaderboard import SiteLeaderboard
import db.db_error_helper as ERROR

def post_fieldcheck(data):
    valid_field = ['userid', 'title', 'content', 'posttime', 'posttype', 'puzzleid']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding post: invalid field provided.")
    return


def get_post(Post, data):
    # get post data by postid
    if 'postid' not in data:
        raise ERROR.DB_Error("Error fetching post: postid not provided.")
    with Session() as s:
        try:
            stmt = select(Post.userid, Post.title, Post.content, Post.posttime, Post.posttype, Post.puzzleid).where(
                Post.postid == data['postid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error fetching post: No post found.")


def add_post(Post, data):
    # this function need to be called after add_puzzle, since puzzleid in post table is a FK
    if 'userid' not in data:
        raise ERROR.DB_Error("Error adding post: userid not provided.")
    if 'posttime' not in data:
        raise ERROR.DB_Error("Error adding post: posttime not provided.")
    with Session() as s:
        try:
            post_fieldcheck(data)
            post = Post(**data)
            s.add(post)
            s.commit()
        # Need to test which exception will be raised in this method, for now use generic Expection
        except Exception as e:
            raise ERROR.DB_Error(f"Error adding post: {e}") from e
        try:
            # update siteleaderboard
            # ~~not sure whether to use slb.postcount or just slb, need to test~~
            # slb is the answer: need to use the object itself, not the attribute
            stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == data['userid'])
            origin = s.execute(stmt).scalar_one()
            origin.postcount = origin.postcount + 1
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"Error updating siteleaderboard: {e}") from e
    return "Post added successfully."


def edit_post(Post, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("Error editing post: postid not provided.")
    # updated time should also be parsed, as "posttime"
    if 'posttime' not in data:
        raise ERROR.DB_Error("Error editing post: posttime not provided.")
    with Session() as s:
        try:
            # everything not be altered should stay the same
            stmt = select(Post).where(Post.postid == data['postid'])
            origin = s.execute(stmt).scalar_one()
            origin.title = data.get('title', origin.title)
            origin.content = data.get('content', origin.content)
            origin.posttime = data.get('posttime', origin.posttime)
            origin.puzzleid = data.get('puzzleid', origin.puzzleid)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error updating post: No post found.")
        return "Post updated successfully."


def delete_post(Post, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("Error deleting post: postid not provided.")
    with Session() as s:
        try:
            stmt = delete(Post).where(Post.postid == data['postid'])
            s.execute(stmt)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error deleting post: No post found.")
        return "Post deleted successfully."
