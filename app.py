from flask import request, render_template, send_from_directory, make_response
from models import db
from email_utils import send_email, store_email
from config import app, metrics, limiter
from datetime import datetime, timedelta
from collections import defaultdict
from constants import DOMAIN_NAME, EMAIL_LIMIT
from flask import jsonify


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
@limiter.limit(f"{EMAIL_LIMIT} per day")
def email_endpoint():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email_address = request.form.get('email')
    subject = request.form.get('subject')
    message_content = request.form.get('message')

    store_email(db, fname, lname, email_address, subject, message_content)

    if not app.config['TESTING']:
        response = send_email(fname, lname, email_address, subject, message_content)
        if "error" in response.json:
            app.logger.error(response.json['error'])
        else:
            app.logger.info(response.json["message"])
    else:
        response = jsonify({"message": "Simulated email sent successfully!"})

    return response
@app.route('/robots.txt')
@metrics.do_not_track()
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/sitemap.xml', methods=['GET'])
@metrics.do_not_track()
def sitemap():
    """Generate sitemap.xml. Makes a list of urls/subfolder with date modified and priority."""
    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)
    page_priority = defaultdict(lambda: "0.2")

    # Specify the priority of certain pages
    page_priority["/"] = "1.0"

    # The application's URL map is iterated over to find all the routes that allow GET requests and have no arguments
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(
                [f"https://{DOMAIN_NAME}" + str(rule.rule), ten_days_ago, page_priority[str(rule.rule)]]
            )
    # A sitemap is generated using a template and the list of pages
    sitemap_xml = render_template('sitemap_template.xml', pages=pages)

    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response

if __name__ == '__main__':
    if app.config["TMP_SQLITE_DATABASE"]:
        app.logger.info("Creating temporary SQLite database.")
        with app.app_context():
            db.create_all()
    app.run(host="0.0.0.0", port=2387, debug=False)