import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR


def is_failure(Failure, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("postid not provided.")
    with Session() as s:
        try:
            stmt = select(Failure).where(Failure.userid == data['userid'], Failure.postid == data['postid'])
            res = s.execute(stmt).fetchone()
            return res is not None
        except sqlalchemy.exc.NoResultFound:
            return False
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e
