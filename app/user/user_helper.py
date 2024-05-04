import app.user.user_db_helper as User_DB
from app.models.user import User

def check_password(db_user_password, provided_password):
    """Check password hash"""
    return db_user_password == provided_password

def authenticate_user(username, password):
    """Authenticate user on login"""
    user = User_DB.get_user(User, {'username': username})
    if user is None:
        return False
    return check_password(user.password, password)


def register_user(username, password, email="hello_world@gmail.com", avatar="hello"):
    data = {
        "username": username,
        "password": password,
        "email": email,
        "avatar": avatar
    }
    return User_DB.add_user(User, data)
