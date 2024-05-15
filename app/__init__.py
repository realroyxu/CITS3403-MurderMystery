from flask import Flask
from app.blueprints.user import user_bp
from app.blueprints.index import index_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcde'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/ormtest.db'

    app.register_blueprint(user_bp)
    app.register_blueprint(index_bp)

    return app
