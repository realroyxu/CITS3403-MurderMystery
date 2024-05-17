from . import puzzle_db_helper as Puzzle_DB
import db.db_error_helper as ERROR
from app.models.puzzle import Puzzle
from app.models.failure import Failure
from datetime import datetime
from app.blueprints.post import post_helper
from app.blueprints.leaderboard import siteleaderboard_helper as slb_helper

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
    if 'guesstext' not in data:
        raise ERROR.DB_Error("guesstext not provided.")
    if "postid" not in data:
        raise ERROR.DB_Error("postid not provided.")
    if "userid" not in data:
        raise ERROR.DB_Error("userid not provided.")
    try:
        puzzleid = post_helper.get_post({"postid": data["postid"]})["puzzleid"]
        data["puzzleid"] = puzzleid
        puzzle = Puzzle_DB.get_puzzle(Puzzle, data)
        if puzzle['puzzleanswer'] == data['guesstext']:
            # need to set post as solved (on post table) & closed (checked by api maybe) & log record on slb
            post_helper.edit_post({"postid": data["postid"], "posttype": "solved"})
            slb_helper.new_solve(data["userid"])
            return True
        # need to log user as killed at failure table
        else:
            Puzzle_DB.puzzle_failed(Failure, data)
            return False
    except ERROR.DB_Error as e:
        raise ERROR.DB_Error(str(e))

