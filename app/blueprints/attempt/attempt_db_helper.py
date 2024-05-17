import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR


def attempt_fieldcheck(data):
    valid_field = ['userid', 'postid', 'progressdata', 'timeelapsed']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("invalid field provided.")
    return


def get_attempt(Attempt, data):
    # get attempt data by (userid, postid)
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    with Session() as s:
        try:
            stmt = select(Attempt.userid, Attempt.postid, Attempt.progressdata, Attempt.timeelapsed).where(
                Attempt.postid == data['postid'] and Attempt.userid == data['userid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No attempt found.")


# in current pattern same user can keep multiple attempts on same post, leaving the rest to backend
# should we keep it or change the logic to update the attempt instead?
def add_attempt(Attempt, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    if 'timeelapsed' not in data:
        raise ERROR.DB_Error("timeelapsed not provided.")
    with Session() as s:
        try:
            attempt_fieldcheck(data)
            attempt = Attempt(**data)
            s.add(attempt)
            s.commit()
        except sqlalchemy.exc.IntegrityError:
            raise ERROR.DB_Error("Only one attempt per post is allowed.")
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e
    return "Attempt added successfully."


def update_attempt(Attempt, data):
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'timeelapsed' not in data:
        raise ERROR.DB_Error("timeelapsed not provided.")
    with Session() as s:
        try:
            stmt = select(Attempt).where(Attempt.postid == data['postid'] and Attempt.userid == data['userid'])
            origin = s.execute(stmt).scalar_one()
            origin.progressdata = data.get('progressdata', origin.progressdata)
            # new elasped time will be calculated before parsing
            # so it's just replacing here
            origin.timeelapsed = origin.timeelapsed + data.get('timeelapsed')
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No attempt found.")

# no delete method here, starting new attempt will just create a new record
