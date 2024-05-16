from flask import render_template, flash, redirect, session, request, url_for
from . import index_bp

user_scores = [
    {"username": "user1", "score": 100},
    {"username": "user2", "score": 200},
    {"username": "user3", "score": 150},
    {"username": "user4", "score": 180},
    {"username": "user5", "score": 120},
]

forum_posts = [
        {
            'id': 1,
            'title': 'I solved it in 0.001s!',
            'content': 'This was a very challenging sudoku but I solved it....',
            'image_url': '../../static/images/sudoku.png',
            'comments': [
                {'author': 'User1', 'text': 'Great post!'},
                {'author': 'User2', 'text': 'Thanks for sharing!'},
                {'author': 'User3', 'text': 'Interesting read.'}
            ]
        },
        {
            'id': 2,
            'title': 'CITS3403 is uh',
            'content': 'CITS3403 is so fun!!!!! just kidding....',
            'image_url': '../../static/images/sudoku.png',
            'comments': [
                {'author': 'User4', 'text': 'I love Sudoku!'},
                {'author': 'User5', 'text': 'Can you share more tips?'}
            ]
        }
    ]

@index_bp.route('/', methods=['GET'])
@index_bp.route('/index', methods=['GET'])
def index():
    css_file_path = url_for('static', filename='index_style.css')
    return render_template('index.html', css_file_path=css_file_path, forum_posts=forum_posts)


@index_bp.route('/createSudoku', methods=['GET'])
def createSudoku():
    return render_template('createSudoku.html')

@index_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    return render_template('leaderboard.html')
