import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR


def get_user(User, data):
    """Get one user"""
    with Session() as s:
        try:
            stmt = select(User).where(User.username == data['username'])
            return s.execute(stmt).one()[0]
        except Exception:
            raise ERROR.DB_Error("User not found")


def get_all(User, data):
    """Get all users"""
    with Session() as s:
        stmt = select(User.userid, User.username, User.email, User.avatar).where(User.userid == data['userid'])
        try:
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except Exception:
            raise ERROR.DB_Error("Users not found")


def add_user(User, data):
    """Add new user"""
    with Session() as s:
        try:
            user = User(**data)
            s.add(user)
            s.commit()
        except Exception:
            raise ERROR.DB_Error("Failed to register User")


def update_user(User, data):
    """Update user data"""
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.avatar = data.get('avatar', user.avatar)
            s.commit()
            return "User updated successfully."
        except Exception:
            raise ERROR.DB_Error("Failed to update user")


def delete_user(User, data):
    """Delete user"""
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            s.delete(user)
            s.commit()
        except Exception:
            raise ERROR.DB_Error("Failed to delete user")
    return "User deleted successfully."


def change_password(User, data):
    """Change user password"""
    with Session() as s:
        try:
            stmt = select(User).where(User.userid == data['userid'])
            user = s.execute(stmt).scalar_one()
            user.password = data['password']
            s.commit()
        except Exception:
            raise ERROR.DB_Error("Failed to change password")
