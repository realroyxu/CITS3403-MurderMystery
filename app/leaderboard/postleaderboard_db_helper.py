import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
from app.models.siteleaderboard import SiteLeaderboard


def postleaderboard_fieldcheck(data):
    valid_field = ['userid', 'postid']
    # rank not needed, will be calculated here
    if not all(field in valid_field for field in data.keys()):
        raise RuntimeError("Error adding postleaderboard: invalid field provided.")
    return


# record will only be added when the user has completed the puzzle
# so no need to have update method
# this will also trigger an update to the siteleaderboard [solvecount]
def add_plbrecord(PostLeaderboard, data):
    if 'userid' not in data:
        raise RuntimeError("Error adding postleaderboard: userid not provided.")
    if 'postid' not in data:
        raise RuntimeError("Error adding postleaderboard: postid not provided.")
    # rank will be calculated here, and need testing
    with Session() as s:
        try:
            postleaderboard_fieldcheck(data)
            stmt = select(func.max(PostLeaderboard.rank)).where(PostLeaderboard.postid == data['postid'])
            data['rank'] = s.execute(stmt).scalar_one().rank + 1
            plbrecord = PostLeaderboard(**data)
            s.add(plbrecord)
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error adding postleaderboard: {e}") from e
        try:
            # update siteleaderboard
            stmt = select(SiteLeaderboard.solvecount).where(SiteLeaderboard.userid == data['userid'])
            origin = s.execute(stmt).scalar_one()
            origin.solvecount = origin.solvecount + 1
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error updating siteleaderboard: {e}") from e
    return "PostLeaderboard added successfully."


def get_plbrecord(PostLeaderboard, data):
    if 'postid' not in data:
        raise RuntimeError("Error fetching postleaderboard: recordid not provided.")
    with Session() as s:
        try:
            stmt = select(PostLeaderboard).where(PostLeaderboard.recordid == data['postid'])
            res = s.execute(stmt).all()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching postleaderboard: No record found.")