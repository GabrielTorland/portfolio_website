from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Configure Flask logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('portfolio_website.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.info("Logger configured.")

# Required for swag reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Recaptcha keys
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY')

# CSRF protection
app.config['SECRET_KEY'] = os.environ.get('PORTFOLIO_WEBSITE_SECRET_KEY')
csrf = CSRFProtect(app)

redis_url = os.getenv('REDIS_URL')

if redis_url:
    app.logger.info(f"Using Redis at {redis_url}")
    limiter = Limiter(app=app, key_func=get_remote_address, storage_uri=redis_url, default_limits=["100 per day"])
else:
    app.logger.warning("Redis URL not set. Using in-memory rate limiting.")
    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per day"])
