from . import siteleaderboard_db_helper as Slb_DB
import db.db_error_helper as ERROR
from app.models.siteleaderboard import SiteLeaderboard as Slb


def get_slb_by_post():
    """Get siteleaderboard ordered by postcount"""
    try:
        return Slb_DB.get_slb_by_post(Slb)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def get_slb_by_solve():
    """Get siteleaderboard ordered by solvecount"""
    try:
        return Slb_DB.get_slb_by_solve(Slb)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
