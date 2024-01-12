from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from logging.config import dictConfig

# Configure logging
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "worldClock.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)

app = Flask(__name__)
# Configure ProxyFix with the appropriate number of proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure database
database_uri = os.getenv('DATABASE_URI')
if database_uri:
    app.logger.info(f"Using provided database URI")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config["TMP_SQLITE_DATABASE"] = False
else:
    app.logger.info(f"Using temporary SQLite database")
    app.config["TMP_SQLITE_DATABASE"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'

# Do not track modifications to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup database
db = SQLAlchemy(app)

# Configure rate limiting
redis_url = os.getenv('REDIS_URL')
if redis_url:
    app.logger.info(f"Using provided Redis URL")
    limiter = Limiter(app=app, key_func=get_remote_address, storage_uri=redis_url, default_limits=["100 per day"])
else:
    app.logger.info(f"Using default rate limiting")
    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per day"])
