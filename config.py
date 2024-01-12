from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)
# Configure ProxyFix with the appropriate number of proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
database_uri = os.getenv('DATABASE_URI')
if database_uri:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config["TMP_SQLITE_DATABASE"] = False
else:
    app.config["TMP_SQLITE_DATABASE"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL')

db = SQLAlchemy(app)

if redis_url:
    limiter = Limiter(app=app, key_func=get_remote_address, storage_uri=redis_url, default_limits=["100 per day"])
else:
    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per day"])
