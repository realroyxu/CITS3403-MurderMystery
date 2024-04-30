from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcde'

# Your routes and other configurations
from app import routes
