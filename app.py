from flask import request, render_template
from models import db, Email
from email_utils import send_email
from config import app, limiter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
@limiter.limit("100 per day")
def email_endpoint():
    return send_email(request, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=2387, debug=False)