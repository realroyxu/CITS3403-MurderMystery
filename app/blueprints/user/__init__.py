from flask import Blueprint

user_bp = Blueprint('user', __name__)

# routes has to be imported after user_bp is created or else there will be a "circular import error"
from . import routes
