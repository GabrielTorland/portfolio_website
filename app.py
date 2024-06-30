from flask import request, render_template, send_from_directory, make_response
from models import db
from email_utils import send_email, store_email
from config import app, limiter
from datetime import datetime, timedelta
from collections import defaultdict
from constants import DOMAIN_NAME, EMAIL_LIMIT
from forms import EmailForm
import requests

@app.route('/')
def index():
    with open("skills_links.txt", "r") as file:
        skills_links = file.readlines()
    return render_template('index.html', skills_links=skills_links)

@app.route('/send_email', methods=['POST'])
@limiter.limit(f"{EMAIL_LIMIT} per day")
def email_endpoint():
    form = EmailForm(request.form)
    if not form.validate_on_submit():
        return {"message": form.errors}, 400

    recaptcha_response = request.form['g-recaptcha-response']

    recaptcha_data = {
        'secret': app.config['RECAPTCHA_SECRET_KEY'],
        'response': recaptcha_response
    }

    recaptcha_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_data)
    recaptcha_response = recaptcha_response.json()


    if not recaptcha_response.get('success'):
        return {"message": "Recaptcha validation failed."}, 400

    fname = form.fname.data
    lname = form.lname.data
    email_address = form.email.data
    subject = form.subject.data
    message_content = form.message.data

    store_email(db, fname, lname, email_address, subject, message_content)

    if not app.config['TESTING']:
        return send_email(fname, lname, email_address, subject, message_content)
    else:
        return {"message": "Simulated email sent successfully!"}, 200

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
    if app.config["TMP_SQLITE_DATABASE"]:
        with app.app_context():
            db.create_all()
    app.run(host="0.0.0.0", port=2387, debug=False)