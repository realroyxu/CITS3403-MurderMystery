import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR


def attempt_fieldcheck(data):
    valid_field = ['userid', 'postid', 'progressdata', 'timeelapsed']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding attempt: invalid field provided.")
    return


def get_attempt(Attempt, data):
    # get attempt data by attemptid
    if 'attemptid' not in data:
        raise ERROR.DB_Error("Error fetching attempt: attemptid not provided.")
    with Session() as s:
        try:
            stmt = select(Attempt.userid, Attempt.postid, Attempt.progressdata, Attempt.timeelapsed).where(
                Attempt.attemptid == data['attemptid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error fetching attempt: No attempt found.")


# in current pattern same user can keep multiple attempts on same post, leaving the rest to backend
# should we keep it or change the logic to update the attempt instead?
def add_attempt(Attempt, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("Error adding attempt: userid not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("Error adding attempt: postid not provided.")
    if 'timeelapsed' not in data:
        raise ERROR.DB_Error("Error adding attempt: timeelapsed not provided.")
    with Session() as s:
        try:
            attempt_fieldcheck(data)
            attempt = Attempt(**data)
            s.add(attempt)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"Error adding attempt: {e}") from e
    return "Attempt added successfully."


def update_attempt(Attempt, data):
    if 'attemptid' not in data:
        raise ERROR.DB_Error("Error updating attempt: attemptid not provided.")
    with Session() as s:
        try:
            stmt = select(Attempt).where(Attempt.attemptid == data['attemptid'])
            origin = s.execute(stmt).scalar_one()
            origin.progressdata = data.get('progressdata', origin.progressdata)
            # new elasped time will be calculated before parsing
            # so it's just replacing here
            origin.timeelapsed = data.get('timeelapsed', origin.timeelapsed)
            s.commit()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("Error updating attempt: No attempt found.")
        return "Attempt updated successfully."

# no delete method here, starting new attempt will just create a new record
