import sqlalchemy.exc
from sqlalchemy import *
from db.database import Session
import db.db_error_helper as ERROR


# siteleaderboard is basically manipulated by other tables

def get_slb_by_post(SiteLeaderboard):
    with Session() as s:
        stmt = select(SiteLeaderboard.userid, SiteLeaderboard.postcount, SiteLeaderboard.solvecount).order_by(
            SiteLeaderboard.postcount.desc())
        res = s.execute(stmt).all()
        if res:
            return [dict(row._mapping) for row in res]
        else:
            raise ERROR.DB_Error("No record found")


def get_slb_by_solve(SiteLeaderboard):
    with Session() as s:
        stmt = select(SiteLeaderboard.userid, SiteLeaderboard.postcount, SiteLeaderboard.solvecount).order_by(
            SiteLeaderboard.solvecount.desc())
        res = s.execute(stmt).all()
        if res:
            return [dict(row._mapping) for row in res]
        else:
            raise ERROR.DB_Error("No record found")
