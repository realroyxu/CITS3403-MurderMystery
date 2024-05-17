import app.blueprints.user.user_db_helper as User_DB
import db.db_error_helper as ERROR
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def hash_password(self, password):
        """Hash a password for storing."""
        password_hash = generate_password_hash(password)
        return password_hash

    def check_password(self, hashed_password, given_password):
        """Check hashed password."""
        return check_password_hash(hashed_password, given_password)

    def authenticate_user(self, username, password):
        """Authenticate user on login"""
        user = User_DB.get_user(User, {'username': username})
        return self.check_password(user.password, password)

    def change_password(self, username, old_password, new_password):
        """Change password for user"""
        user = User_DB.get_user(User, {'username': username})
        if self.check_password(user.password, old_password):
            user_id = User_DB.get_userid(User, {'username': username})
            data = {
                "userid": user_id,
                "password": self.hash_password(new_password)
            }
            User_DB.change_password(User, data)
            return True
        return False

    def register_user(self, username, password, email="hello_world@gmail.com", avatarid=0):
        data = {
            "username": username,
            "password": self.hash_password(password),
            "email": email,
            "avatarid": avatarid
        }
        return User_DB.add_user(User, data)

    def change_avatar(self, userid, avatarid):
        """Change user avatar"""
        try:
            return User_DB.update_user(User, {"userid": userid, "avatarid": avatarid})
        except ERROR.DB_Error as e:
            raise ERROR.DB_Error(str(e))

    def get_userid(self, username):
        """Get user id by username"""
        try:
            return User_DB.get_userid(User, {"username": username})
        except ERROR.DB_Error as e:
            raise ERROR.DB_Error(str(e))

    def get_username(self, userid):
        """Get username by user id"""
        try:
            return User_DB.get_username(User, {"userid": userid})
        except ERROR.DB_Error as e:
            raise ERROR.DB_Error(str(e))


user_service = UserService()


