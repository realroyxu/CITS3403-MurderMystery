from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.puzzle import Puzzle
from app.models.attempt import Attempt
from app.models.postleaderboard import PostLeaderboard
import app.user.user_db_helper as udb
import app.post.post_db_helper as pdb
import app.puzzle.puzzle_db_helper as pzdb
import app.attempt.attempt_db_helper as atdb
import app.comment.comment_db_helper as cdb
import app.leaderboard.postleaderboard_db_helper as pldb


def usertest():
    print(udb.get_user(User, {'username': 'aifert'}))
    print('*********************************')
    print(udb.get_all(User, {'userid': 1}))
    print('*********************************')
    print(udb.add_user(User, {'username': 'test1', 'password': 'test1', 'email': '', 'avatar': ''}))
    print('*********************************')
    print(udb.update_user(User, {'userid': 2, 'username': 'test0', 'password': 'test1', 'email': '', 'avatar': ''}))
    print('*********************************')
    print(udb.delete_user(User, {'userid': 2}))
    print('*********************************')


def posttest():
    print(pdb.add_post(Post,
                       {'userid': 3, 'title': 'test1', 'content': 'test1', 'posttime': '16:21', 'posttype': 'easy',
                        'puzzleid': 1}))
    print('*********************************')
    print(pdb.get_post(Post, {'postid': 7}))
    print('*********************************')
    print(
        pdb.edit_post(Post, {'postid': 7, 'title': 'test0', 'content': 'test0', 'posttime': '06:21', 'posttype': 'hard',
                             'puzzleid': 2}))
    print('*********************************')
    print(pdb.delete_post(Post, {'postid': 3}))
    print('*********************************')


def puzzletest():
    print(pzdb.add_puzzle(Puzzle, {'userid': 3, 'createtime': '16:49', 'puzzledata': 'DATA', 'category': 'medium'}))
    print('*********************************')
    print(pzdb.get_puzzle(Puzzle, {'puzzleid': 6}))
    print('*********************************')
    print(pzdb.update_puzzle(Puzzle, {'puzzleid': 7, 'userid': 3, 'createtime': '06:49', 'puzzledata': 'DATA0',
                                      'category': 'hard'}))
    print('*********************************')


def attempttest():
    print(atdb.add_attempt(Attempt, {'userid': 3, 'postid': 7, 'progressdata': 'DATA', 'timeelapsed': 120}))
    print('*********************************')
    print(atdb.get_attempt(Attempt, {'attemptid': 6}))
    print('*********************************')
    print(atdb.update_attempt(Attempt, {'attemptid': 7, 'userid': 3, 'postid': 7, 'progressdata': 'DATA0',
                                        'timeelapsed': 180}))
    print('*********************************')


def commenttest():
    print(cdb.add_comment(Comment, {'userid': 3, 'postid': 7, 'commenttext': 'test1', 'commenttime': '17:34'}))
    print('*********************************')
    print(cdb.get_comment(Comment, {'commentid': 6}))
    print('*********************************')
    print(cdb.edit_comment(Comment, {'commentid': 7, 'userid': 3, 'postid': 7, 'commenttext': 'test0',
                                     'commenttime': '07:21'}))
    # print('*********************************')


def plbtest():
    print(pldb.add_plbrecord(PostLeaderboard, {'userid': 3, 'postid': 7}))
    print('*********************************')
    print(pldb.get_plbrecord(PostLeaderboard, {'postid': 7}))
    print('*********************************')


try:
    usertest()
    # posttest()
    # puzzletest()
    # attempttest()
    # commenttest()
    # plbtest()
    pass
except Exception as e:
    print(e)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
