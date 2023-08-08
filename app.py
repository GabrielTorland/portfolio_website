from flask import Flask, request, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError
from email.mime.text import MIMEText
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from datetime import datetime
from flask_limiter.storage import RedisStorage
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL')
storage = RedisStorage(redis_url)

db = SQLAlchemy(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=redis_url,
    default_limits=["100 per day"]
)

# Extracting SMTP configurations from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_RECEIVER = os.getenv('SMTP_RECEIVER')

HTML_TEMPLATE = '''Your HTML form content here'''  # Replace with your HTML form

class Email(db.Model):
    """Email model for storing email details."""
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_email', methods=['POST'])
@limiter.limit("100 per day")
def send_email():
    """Endpoint to send emails."""
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email_address = request.form.get('email')
    subject = request.form.get('subject')
    message_content = request.form.get('message')

    email_entry = Email(fname=fname, lname=lname, email=email_address, subject=subject, message=message_content)
    db.session.add(email_entry)
    db.session.commit()

    msg = MIMEText(f"From: {fname} {lname}\nEmail: {email_address}\n\n{message_content}")
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_RECEIVER
    
    try:
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, SMTP_RECEIVER, msg.as_string())
        return jsonify({"message": "Email sent successfully!"})
    except SMTPConnectError:
        return jsonify({"error": "Failed to connect to the SMTP server."})
    except SMTPAuthenticationError:
        return jsonify({"error": "SMTP authentication failed. Check your username and password."})
    except SMTPRecipientsRefused:
        return jsonify({"error": "The recipient(s) was refused by the server."})
    except SMTPSenderRefused:
        return jsonify({"error": "The sender was refused by the server."})
    except SMTPDataError:
        return jsonify({"error": "The server replied with an unexpected error code."})
    except Exception as e:
        return jsonify({"error": f"Error sending email: {str(e)}"})


@app.route('/emails', methods=['GET'])
def get_emails():
    """Endpoint to fetch all email entries in JSON format."""
    emails = Email.query.all()
    return jsonify([{
        'id': email.id,
        'fname': email.fname,
        'lname': email.lname,
        'email': email.email,
        'subject': email.subject,
        'message': email.message,
        'date_sent': email.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
    } for email in emails])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=2387, debug=False)