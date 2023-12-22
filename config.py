from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL')

db = SQLAlchemy(app)
limiter = Limiter(app=app, key_func=get_remote_address, storage_uri=redis_url, default_limits=["100 per day"])