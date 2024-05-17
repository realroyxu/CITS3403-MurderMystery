from . import puzzle_db_helper as Puzzle_DB
import db.db_error_helper as ERROR
from app.models.puzzle import Puzzle
from datetime import datetime


def get_puzzle(data):
    """Get puzzle data by puzzleid"""
    try:
        return Puzzle_DB.get_puzzle(Puzzle, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def add_puzzle(data):
    """Add new puzzle"""
    data['updatetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Puzzle_DB.add_puzzle(Puzzle, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def edit_puzzle(data):
    """Edit puzzle"""
    data['updatetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        return Puzzle_DB.edit_puzzle(Puzzle, data)
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))


def verify_answer(data) -> bool:
    """Verify answer"""
    if 'puzzleanswer' not in data:
        raise ERROR.DB_Error("puzzleanswer not provided.")
    try:
        puzzle = Puzzle_DB.get_puzzle(Puzzle, data)
        if puzzle['puzzleanswer'] == data['puzzleanswer']:
            return True
        return False
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))
