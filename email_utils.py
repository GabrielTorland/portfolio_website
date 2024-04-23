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
    msg = MIMEText(f"dq8wmC&N89nEF8i^oRo$$Aq6bC\nFrom: {fname} {lname}\nEmail: {email_address}\n\n{message_content}")
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = os.getenv('SMTP_RECEIVER')

    # SMTP server configuration and email sending logic
    try:
        with SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
            server.sendmail(os.getenv('SMTP_USER'), os.getenv('SMTP_RECEIVER'), msg.as_string())
        return jsonify({"message": "Email sent successfully!"}), 200
    except SMTPConnectError:
        return jsonify({"message": "Failed to connect to the SMTP server."}), 500
    except SMTPAuthenticationError:
        return jsonify({"message": "SMTP authentication failed. Check your username and password."}), 500 
    except SMTPRecipientsRefused:
        return jsonify({"message": "The recipient(s) was refused by the server."}), 500
    except SMTPSenderRefused:
        return jsonify({"message": "The sender was refused by the server."}), 500
    except SMTPDataError:
        return jsonify({"message": "The server replied with an unexpected error code."}), 500
    except Exception as e:
        return jsonify({"message": f"Error sending email: {str(e)}"}), 500
