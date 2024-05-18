import sqlalchemy.exc
from sqlalchemy import *
from db.database import Session
import db.db_error_helper as ERROR


# siteleaderboard is basically manipulated by other tables

def get_slb_by_post(SiteLeaderboard, limit):
    with Session() as s:
        stmt = select(SiteLeaderboard.userid, SiteLeaderboard.postcount, SiteLeaderboard.solvecount).order_by(
            SiteLeaderboard.postcount.desc()).limit(limit)
        res = s.execute(stmt).all()
        if res:
            return [dict(row._mapping) for row in res]
        else:
            raise ERROR.DB_Error("No record found")


def get_slb_by_solve(SiteLeaderboard, limit):
    with Session() as s:
        stmt = select(SiteLeaderboard.userid, SiteLeaderboard.postcount, SiteLeaderboard.solvecount).order_by(
            SiteLeaderboard.solvecount.desc()).limit(limit)
        res = s.execute(stmt).all()
        if res:
            return [dict(row._mapping) for row in res]
        else:
            raise ERROR.DB_Error("No record found")


def new_solve(SiteLeaderboard, userid):
    with Session() as s:
        try:
            stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == userid)
            origin = s.execute(stmt).scalar_one()
            origin.solvecount = origin.solvecount + 1
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"error updating siteleaderboard: {e}") from e


def new_post(SiteLeaderboard, userid):
    with Session() as s:
        try:
            stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == userid)
            origin = s.execute(stmt).scalar_one()
            origin.postcount = origin.postcount + 1
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"error updating siteleaderboard: {e}") from e
