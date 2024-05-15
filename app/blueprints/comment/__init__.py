from flask import Blueprint

comment_bp = Blueprint('comment', __name__)

from . import routes
