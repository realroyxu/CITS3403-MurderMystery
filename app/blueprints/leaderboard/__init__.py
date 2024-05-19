from flask import Blueprint

siteleaderboard_bp = Blueprint('siteleaderboard', __name__)

from . import api
from . import routes
