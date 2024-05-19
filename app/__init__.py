from flask import Flask
from dotenv import load_dotenv
import os
from app.blueprints.index import index_bp
from app.blueprints.user import user_bp, user_api_bp
from app.blueprints.post import post_bp, post_api_bp
from app.blueprints.puzzle import puzzle_bp
from app.blueprints.comment import comment_bp
from app.blueprints.attempt import attempt_bp
from app.blueprints.leaderboard import siteleaderboard_bp
from app.blueprints.failure import failure_bp
from flask_sqlalchemy import SQLAlchemy
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

db = SQLAlchemy()

load_dotenv()

def create_app(config_name=''):
    app = Flask(__name__)

    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)

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
    app.register_blueprint(failure_bp)
    return app
