from flask import Blueprint

failure_bp = Blueprint('failure', __name__)

from . import api
