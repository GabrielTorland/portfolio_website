from flask import request, render_template, send_from_directory, make_response
from models import db
from email_utils import send_email, store_email
from config import app, limiter
from datetime import datetime, timedelta
from collections import defaultdict
from constants import DOMAIN_NAME, EMAIL_LIMIT

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
    else:
        response = {"message": "Simulated email sent successfully!"}
    return response

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls/subfolder with date modified and priority."""
    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)
    page_priority = defaultdict(lambda: "0.2")
    page_priority["/"] = "1.0"
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(
                [f"https://{DOMAIN_NAME}" + str(rule.rule), ten_days_ago, page_priority[str(rule.rule)]]
            )

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"    

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2387, debug=False)