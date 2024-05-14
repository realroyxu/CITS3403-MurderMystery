from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcde'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads/'

# Your routes and other configurations
from app import routes
