import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR

from app.models.siteleaderboard import SiteLeaderboard


def user_fieldcheck(data):
    valid_field = ['username', 'password', 'email', 'avatarid']
    # userid shouldn't be provided, bcs functions will convert data to query params
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding user: invalid field provided.")
    return


def get_user(User, data):
    # get userid by username
    with Session() as s:
        try:
            # it has to select(User) in order to retrieve a indexable row object after one()
            stmt = select(User).where(User.username == data['username'])
            result = s.execute(stmt).one()
            return result.User
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("User not found")


def get_userid(User, data):
    """Get user id"""
    with Session() as s:
        try:
            stmt = select(User.userid).where(User.username == data['username'])
            result = s.execute(stmt).one()[0]
            return result
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("User not found")


def get_username(User, data):
    # get username by userid
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            return s.execute(stmt).one()[0].username
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("User not found")


def get_avatarid(User, data):
    # get avatarid by userid
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            return s.execute(stmt).one()[0].avatarid
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("User not found")


def validate_user(User, data):
    # login validation
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            res = s.execute(stmt).one()[0].password
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("User not found")
        if res == data['password']:
            return True
        else:
            return False


def get_all(User, data):
    # get all user data by userid, except password
    # not being used
    with Session() as s:
        stmt = select(User.userid, User.username, User.email, User.avatarid).where(User.userid == data['userid'])
        try:
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except Exception:
            raise ERROR.DB_Error("Users not found")


def add_user(User, data):
    # add new user
    # also need to add entry to siteleaderboards
    if 'username' not in data:
        raise ERROR.DB_Error("Error updating user: username not provided.")
    if 'password' not in data:
        raise ERROR.DB_Error("Error updating user: password not provided.")
    user_fieldcheck(data)
    with Session() as s:
        try:
            user = User(**data)
            s.add(user)
            s.commit()
        except sqlalchemy.exc.IntegrityError as e:
            # raise RuntimeError(f"Error adding user: integrity violated. {e}") from e
            raise ERROR.DB_Error(f"Error adding user: integrity violated. {e}")
        try:
            slbrecord = SiteLeaderboard(userid=user.userid)
            s.add(slbrecord)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"Error encountered: {e}") from e


def update_user(User, data):
    """Update user data"""
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            # scalar() return a instance, update op will be done on this instance
            # has to be scalar() instead of one(), because scalar() returns: <class '__main__.User'>
            # and one() returns:<class 'sqlalchemy.engine.row.Row'>
            origin = s.execute(stmt).scalar_one()
            # if no new value provided, keep the original value
            origin.username = data.get('username', origin.username)
            origin.email = data.get('email', origin.email)
            origin.avatarid = data.get('avatarid', origin.avatarid)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error updating user: No user found.")


def change_password(User, data):
    """Change user password"""
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            user.password = data['password']
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error updating user: No user found.")
        except Exception:
            raise ERROR.DB_Error("Failed to change password")
