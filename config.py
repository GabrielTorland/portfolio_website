from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)
# Configure ProxyFix with the appropriate number of proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL')

db = SQLAlchemy(app)
limiter = Limiter(app=app, key_func=get_remote_address, storage_uri=redis_url, default_limits=["100 per day"])