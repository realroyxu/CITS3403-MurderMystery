from . import postleaderboard_db_helper as Plb_DB
import db.db_error_helper as ERROR
from app.models.postleaderboard import PostLeaderboard as Plb


def get_plb(data):
    """Get postleaderboard by postid"""
    try:
        return Plb_DB.get_plb(Plb, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_record(data):
    """Add new postleaderboard record"""
    try:
        return Plb_DB.add_record(Plb, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))