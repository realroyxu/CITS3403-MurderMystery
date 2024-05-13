import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from db.database import Session


def puzzle_fieldcheck(data):
    valid_field = ['userid', 'puzzledata', 'createtime', 'category']
    if not all(field in valid_field for field in data.keys()):
        raise RuntimeError("Error adding puzzle: invalid field provided.")
    return


def get_puzzle(Puzzle, data):
    if 'puzzleid' not in data:
        raise RuntimeError("Error fetching puzzle: puzzleid not provided.")
    with Session() as s:
        try:
            stmt = select(Puzzle.userid, Puzzle.puzzledata, Puzzle.createtime, Puzzle.category).where(
                Puzzle.puzzleid == data['puzzleid'])
            res = s.execute(stmt).one()
            if res:
                return res._asdict()
        except sqlalchemy.exc.NoResultFound:
            raise RuntimeError("Error fetching puzzle: No puzzle found.")


def add_puzzle(Puzzle, data):
    if 'userid' not in data:
        raise RuntimeError("Error adding puzzle: userid not provided.")
    if 'createtime' not in data:
        raise RuntimeError("Error adding puzzle: createtime not provided.")
    puzzle_fieldcheck(data)
    with Session() as s:
        try:
            puzzle = Puzzle(**data)
            s.add(puzzle)
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error adding puzzle: {e}") from e
    return "Puzzle added successfully."


def update_puzzle(Puzzle, data):
    if 'puzzleid' not in data:
        raise RuntimeError("Error updating puzzle: puzzleid not provided.")
    with Session() as s:
        try:
            stmt = select(Puzzle).where(Puzzle.puzzleid == data['puzzleid'])
            origin = s.execute(stmt).scalar_one()
            origin.puzzledata = data.get('puzzledata', origin.puzzledata)
            origin.createtime = data.get('createtime', origin.createtime)
            origin.category = data.get('category', origin.category)
            s.commit()
        except Exception as e:
            raise RuntimeError(f"Error updating puzzle: {e}") from e
    return "Puzzle updated successfully."

# same as attempt, no need to delete puzzle record
