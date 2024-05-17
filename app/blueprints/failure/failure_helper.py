import db.db_error_helper as ERROR
from . import failure_db_helper as Failure_DB
from app.models.failure import Failure


def is_failure(data):
    """Check if user is failed on a post"""
    try:
        return Failure_DB.is_failure(Failure, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
