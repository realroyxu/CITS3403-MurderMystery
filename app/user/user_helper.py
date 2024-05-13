import app.user.user_db_helper as User_DB
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
            user.password = self.hash_password(new_password)
            User_DB.add_user(User, user)
            return True
        return False

    def register_user(self, username, password, email="hello_world@gmail.com", avatar="hello"):
        data = {
            "username": username,
            "password": self.hash_password(password),
            "email": email,
            "avatar": avatar
        }
        return User_DB.add_user(User, data)


user_service = UserService()
