from flask import Blueprint

post_bp = Blueprint('post', __name__)
post_api_bp = Blueprint('post_api', __name__)

from . import routes
from . import api
