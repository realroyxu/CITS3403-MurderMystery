from flask import Blueprint

attempt_bp = Blueprint('attempt', __name__)

from . import routes
