import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
from app.models.siteleaderboard import SiteLeaderboard
import db.db_error_helper as ERROR


def postleaderboard_fieldcheck(data):
    valid_field = ['userid', 'postid']
    # rank not needed, will be calculated here
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding postleaderboard: invalid field provided.")
    return


# record will only be added when the user has completed the puzzle
# so no need to have update method
# this will also trigger an update to the siteleaderboard [solvecount]
# Should we keep them in 2 independent transactions? Or make slb to query plb's record?

# Currently this function allows user to insert multiple records for the same post
# Should we keep it?
def add_record(PostLeaderboard, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("Error adding postleaderboard: userid not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("Error adding postleaderboard: postid not provided.")
    # rank will be calculated here, and need testing
    with Session() as s:
        try:
            postleaderboard_fieldcheck(data)
            stmt = select(func.max(PostLeaderboard.rank)).where(PostLeaderboard.postid == data['postid'])
            if not s.execute(stmt).scalar_one():
                data['rank'] = 1
            else:
                data['rank'] = s.execute(stmt).scalar_one() + 1
            plbrecord = PostLeaderboard(**data)
            s.add(plbrecord)
            # should wait for slb's commit
            # s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"Error adding postleaderboard: {e}") from e
        try:
            # update siteleaderboard
            stmt = select(SiteLeaderboard).where(SiteLeaderboard.userid == data['userid'])
            origin = s.execute(stmt).scalar_one()
            origin.solvecount = origin.solvecount + 1
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"Error updating siteleaderboard: {e}") from e
    return "PostLeaderboard added successfully."


# get plbrecord by postid
def get_plb(PostLeaderboard, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("Error fetching postleaderboard: postid not provided.")
    with Session() as s:
        try:
            stmt = select(PostLeaderboard.userid, PostLeaderboard.rank).where(
                PostLeaderboard.postid == data['postid'])
            res = s.execute(stmt).all()
            if res:
                return [dict(row._mapping) for row in res]
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error fetching postleaderboard: No record found.")
