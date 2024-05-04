import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session


def get_user(User, data):
    # get user id by username
    if 'username' not in data:
        raise RuntimeError("Error updating user: username not provided.")
    with Session() as s:
        try:
            stmt = select(User).where(User.username == data['username'])
            return s.execute(stmt).one()[0]
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching user: No user found.")
    # need error hanlding


def get_all(User, data):
    # get users data by userid, without password
    if 'userid' not in data:
        raise RuntimeError("Error updating user: userid not provided.")
    with Session() as s:
        stmt = select(User.userid, User.username, User.email, User.avatar).where(User.userid == data['userid'])
        try:
            res = s.execute(stmt).one()
            if res:
                # _asdict() is a dict-ize method of RowProxy
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching user: No user found.")

def add_user(User, data):
    # add new user
    if 'username' not in data:
        raise RuntimeError("Error updating user: username not provided.")
    if 'password' not in data:
        raise RuntimeError("Error updating user: password not provided.")
    for item in data.keys():
        if item not in ('username', 'password', 'email', 'avatar'):
            raise RuntimeError("Error updating user: invalid field provided.")
    with Session() as s:
        try:
            user = User(**data)
            s.add(user)
            s.commit()
        except sqlalchemy.exc.IntegrityError as e:
            raise RuntimeError(f"Error adding user: integrity violated. {e}") from e


def update_user(User, data):
    # update user's profile
    if 'userid' not in data:
        raise RuntimeError("Error updating user: userid not provided.")
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            # scalar() return a instance, update op will be done on this instance
            # has to be scalar() instead of one(), because scalar() returns: <class '__main__.User'>
            # and one() returns:<class 'sqlalchemy.engine.row.Row'>
            user = s.execute(stmt).scalar_one()
            # if no new value provided, keep the original value
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.avatar = data.get('avatar', user.avatar)
            s.commit()
            return "User updated successfully."
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error updating user: No user found.")


def delete_user(User, data):
    if 'userid' not in data:
        raise RuntimeError("Error updating user: userid not provided.")
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            s.delete(user)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error updating user: No user found.")
    return "User deleted successfully."


def change_password(User, data):
    if 'userid' not in data:
        raise RuntimeError("Error updating user: userid not provided.")
    if 'password' not in data:
        raise RuntimeError("Error updating user: password not provided.")
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            user.password = data['password']
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error updating user: No user found.")
