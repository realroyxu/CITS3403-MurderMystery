import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session


def attempt_fieldcheck(data):
    valid_field = ['userid', 'puzzleid', 'progressdata', 'timeelapsed']
    if not all(field in valid_field for field in data.keys()):
        raise RuntimeError("Error adding attempt: invalid field provided.")
    return


def get_attempt(Attempt, data):
    # get attempt data by attemptid
    if 'attemptid' not in data:
        raise RuntimeError("Error fetching attempt: attemptid not provided.")
    with Session() as s:
        try:
            stmt = select(Attempt).where(Attempt.attemptid == data['attemptid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching attempt: No attempt found.")


def add_attempt(Attempt, data):
    if 'userid' not in data:
        raise RuntimeError("Error adding attempt: userid not provided.")
    if 'puzzleid' not in data:
        raise RuntimeError("Error adding attempt: puzzleid not provided.")
    if 'timeelapsed' not in data:
        raise RuntimeError("Error adding attempt: timeelapsed not provided.")
    with Session() as s:
        try:
            attempt_fieldcheck(data)
            attempt = Attempt(**data)
            s.add(attempt)
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error adding attempt: {e}") from e
    return "Attempt added successfully."


def update_attempt(Attempt, data):
    if 'attemptid' not in data:
        raise RuntimeError("Error updating attempt: attemptid not provided.")
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
            raise RuntimeError("Error updating attempt: No attempt found.")
        return "Attempt updated successfully."


# no delete method here, starting new attempt will just create a new record


