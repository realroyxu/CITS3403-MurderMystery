from . import attempt_db_helper as Attempt_DB
from db import db_error_helper as ERROR
from app.models.attempt import Attempt


def get_attempt(data):
    """Get attempt data by attemptid"""
    try:
        return Attempt_DB.get_attempt(Attempt, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_attempt(data):
    """Add new attempt"""
    try:
        return Attempt_DB.add_attempt(Attempt, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def update_attempt(data):
    """Update attempt"""
    try:
        return Attempt_DB.update_attempt(Attempt, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))

