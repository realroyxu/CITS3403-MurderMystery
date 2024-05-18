from . import siteleaderboard_db_helper as Slb_DB
import db.db_error_helper as ERROR
from app.models.siteleaderboard import SiteLeaderboard as Slb


def get_slb_by_post(limit):
    """Get siteleaderboard ordered by postcount"""
    try:
        return Slb_DB.get_slb_by_post(Slb, limit)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_slb_by_solve(limit):
    """Get siteleaderboard ordered by solvecount"""
    try:
        return Slb_DB.get_slb_by_solve(Slb, limit)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def new_solve(userid):
    """Add solve count"""
    try:
        return Slb_DB.new_solve(Slb, userid)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def new_post(userid):
    """Add post count"""
    try:
        return Slb_DB.new_post(Slb, userid)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
