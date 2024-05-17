from flask import Blueprint

siteleaderboard_bp = Blueprint('siteleaderboard', __name__)
postleaderboard_bp = Blueprint('postleaderboard', __name__)

from . import routes
