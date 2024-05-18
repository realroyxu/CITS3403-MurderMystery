import sqlalchemy.exc
from sqlalchemy import *
from db.database import Session
from app.models.siteleaderboard import SiteLeaderboard
import db.db_error_helper as ERROR


def post_fieldcheck(data):
    valid_field = ['userid', 'title', 'content', 'posttime', 'posttype', 'puzzleid']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("invalid field provided.")
    return


def get_post(Post, data):
    # get post data by postid
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    with Session() as s:
        try:
            stmt = select(Post.postid, Post.userid, Post.title, Post.content, Post.posttime, Post.posttype,
                          Post.puzzleid, Post.postimage).where(
                Post.postid == data['postid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No post found.")

def get_all_posts(Post):
    """Get all posts in database"""
    with Session() as s:
        try:
            stmt = select(Post.postid, Post.userid, Post.title, Post.content, Post.posttime, Post.posttype,
                          Post.puzzleid, Post.postimage).order_by(Post.posttime.desc())
            res = s.execute(stmt).all()
            if res:
                return [row._asdict() for row in res]
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No post found.")


def add_post(Post, data):
    # this function need to be called after add_puzzle, since puzzleid in post table is a FK
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'posttime' not in data:
        raise ERROR.DB_Error("posttime not provided.")
    with Session() as s:
        try:
            post_fieldcheck(data)
            post = Post(**data)
            s.add(post)
            s.commit()
            s.refresh(post)
            # get this new post's id
            # sqlalchemy will just assign new postid directly to this post object
            return post.postid
        # Need to test which exception will be raised in this method, for now use generic Expection
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e

        # UPDATE: MOVING TO SLB_HELPER NOW, PLEASE KEEP IT FOR NOW
        # try:
        #     # update siteleaderboard
        #     # ~~not sure whether to use slb.postcount or just slb, need to test~~
        #     # slb is the answer: need to use the object itself, not the attribute
        #     stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == data['userid'])
        #     origin = s.execute(stmt).scalar_one()
        #     origin.postcount = origin.postcount + 1
        #     s.commit()
        # except Exception as e:
        #     raise ERROR.DB_Error(f"error updating siteleaderboard: {e}") from e


def edit_post(Post, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    # updated time should also be parsed, as "posttime"
    if 'posttime' not in data:
        raise ERROR.DB_Error("posttime not provided.")
    with Session() as s:
        try:
            # everything not be altered should stay the same
            stmt = select(Post).where(Post.postid == data['postid'])
            origin = s.execute(stmt).scalar_one()
            origin.title = data.get('title', origin.title)
            origin.content = data.get('content', origin.content)
            origin.posttime = data.get('posttime', origin.posttime)
            origin.puzzleid = data.get('puzzleid', origin.puzzleid)
            # do we want to restrict to either easy or medium or hard?
            origin.posttype = data.get('posttype', origin.posttype)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No post found.")


def delete_post(Post, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    with Session() as s:
        try:
            # update siteleaderboard: BEFORE DELETING ENTRY IN POST
            stmt = select(Post.userid).where(Post.postid == data['postid'])
            userid = s.execute(stmt).one()
            stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == userid[0])
            origin = s.execute(stmt).scalar_one()
            origin.postcount = origin.postcount - 1
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"error updating siteleaderboard: {e}") from e
        try:
            stmt = delete(Post).where(Post.postid == data['postid'])
            s.execute(stmt)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No post found.")


def add_image(Post, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    if 'postimage' not in data:
        raise ERROR.DB_Error("postimage not provided.")
    with Session() as s:
        try:
            stmt = select(Post).where(Post.postid == data['postid'])
            origin = s.execute(stmt).scalar_one()
            origin.postimage = data.get('postimage', origin.postimage)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No post found.")
