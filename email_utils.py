from flask import jsonify
from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError
from email.mime.text import MIMEText
import os
from models import Email

def store_email(db, fname, lname, email_address, subject, message_content):
    email_entry = Email(fname=fname, lname=lname, email=email_address, subject=subject, message=message_content)
    db.session.add(email_entry)
    db.session.commit()

def send_email(fname, lname, email_address, subject, message_content):
    msg = MIMEText(f"From: {fname} {lname}\nEmail: {email_address}\n\n{message_content}")
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = os.getenv('SMTP_RECEIVER')

    # SMTP server configuration and email sending logic
    try:
        with SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
            server.sendmail(os.getenv('SMTP_USER'), os.getenv('SMTP_RECEIVER'), msg.as_string())
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