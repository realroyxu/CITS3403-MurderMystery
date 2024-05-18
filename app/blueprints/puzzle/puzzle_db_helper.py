import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session
import db.db_error_helper as ERROR


def puzzle_fieldcheck(data):
    valid_field = ['userid', 'puzzledata', 'updatetime', 'category']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding puzzle: invalid field provided.")
    return


def failure_fieldcheck(data):
    valid_field = ['userid', 'postid']
    if not all(field in valid_field for field in data.keys()):
        raise ERROR.DB_Error("Error adding failure: invalid field provided.")
    return


def get_puzzle(Puzzle, data):
    if 'puzzleid' not in data:
        raise ERROR.DB_Error("Error fetching puzzle: puzzleid not provided.")
    with Session() as s:
        try:
            stmt = select(Puzzle.userid, Puzzle.puzzledata, Puzzle.updatetime, Puzzle.category,
                          Puzzle.puzzleanswer).where(
                Puzzle.puzzleid == data['puzzleid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise ERROR.DB_Error("No puzzle found.")


def add_puzzle(Puzzle, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'updatetime' not in data:
        raise ERROR.DB_Error("updatetime not provided.")
    puzzle_fieldcheck(data)
    with Session() as s:
        try:
            puzzle = Puzzle(**data)
            s.add(puzzle)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e


def edit_puzzle(Puzzle, data):
    if 'puzzleid' not in data:
        raise ERROR.DB_Error("puzzleid not provided.")
    with Session() as s:
        try:
            stmt = select(Puzzle).where(Puzzle.puzzleid == data['puzzleid'])
            origin = s.execute(stmt).scalar_one()
            origin.puzzledata = data.get('puzzledata', origin.puzzledata)
            origin.updatetime = data.get('updatetime', origin.updatetime)
            origin.category = data.get('category', origin.category)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e


# same as attempt, no need to delete puzzle record

def puzzle_solved(Puzzle, data):
    pass


def puzzle_failed(Failure, data):
    if 'userid' not in data:
        raise ERROR.DB_Error("userid not provided.")
    if 'postid' not in data:
        raise ERROR.DB_Error("puzzleid not provided.")
    if 'puzzleid' in data:
        del data['puzzleid']
    if 'guesstext' in data:
        del data['guesstext']
    print(data)
    failure_fieldcheck(data)
    with Session() as s:
        try:
            failure = Failure(**data)
            s.add(failure)
            s.commit()
        except Exception as e:
            raise ERROR.DB_Error(f"{e}") from e
