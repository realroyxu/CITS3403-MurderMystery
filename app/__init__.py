from flask import Flask
from app.blueprints.index import index_bp
from app.blueprints.user import user_bp, user_api_bp
from app.blueprints.post import post_bp, post_api_bp
from app.blueprints.puzzle import puzzle_bp
from app.blueprints.comment import comment_bp
from app.blueprints.attempt import attempt_bp
from app.blueprints.leaderboard import siteleaderboard_bp, postleaderboard_bp
from app.blueprints.failure import failure_bp
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcde'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/ormtest.db'

    db.init_app(app)

    app.register_blueprint(index_bp)
    app.register_blueprint(user_api_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(post_api_bp)
    app.register_blueprint(puzzle_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(attempt_bp)
    app.register_blueprint(siteleaderboard_bp)
    app.register_blueprint(postleaderboard_bp)
    app.register_blueprint(failure_bp)
    return app
