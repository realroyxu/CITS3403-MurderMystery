from flask import Blueprint

user_api_bp = Blueprint('user_api', __name__)
user_bp = Blueprint('user', __name__, template_folder='templates')

# routes has to be imported after user_bp is created or else there will be a "circular import error"
from . import api
from . import routes
