from flask import Blueprint

puzzle_bp = Blueprint('puzzle', __name__)

from . import routes
