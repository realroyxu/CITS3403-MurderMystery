import app.user.user_db_helper as User_DB
import db.db_error_helper as ERROR
from app.models.user import User


# password check done on database level

# def check_password(db_user_password, provided_password):
#     """Check password hash"""
#     return db_user_password == provided_password


def authenticate_user(username, password):
    """Authenticate user on login"""
    try:
        userid = User_DB.get_user(User, {"username": username})
        return User_DB.validate_user(User, {"userid": userid, "password": password})
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def register_user(username, password, email, avatar="default.jpg"):
    data = {
        "username": username,
        "password": password,
        "email": email,
        "avatar": avatar
    }
    return User_DB.add_user(User, data)


def change_password(userid, old_password, new_password):
    """Change user password"""
    try:
        if User_DB.validate_user(User, {"userid": userid, "password": old_password}):
            return User_DB.change_password(User, {"userid": userid, "password": new_password})
        else:
            raise ERROR.DB_Error("Incorrect password")
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def change_avatar(userid, avatar):
    """Change user avatar"""
    try:
        return User_DB.update_user(User, {"userid": userid, "avatar": avatar})
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_userid(username):
    """Get user id by username"""
    try:
        return User_DB.get_user(User, {"username": username})
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
