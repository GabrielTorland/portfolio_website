from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError
from email.mime.text import MIMEText
import os

def send_email(fname, lname, email_address, subject, message_content):
    msg = MIMEText(f"dq8wmC&N89nEF8i^oRo$$Aq6bC\nFrom: {fname} {lname}\nEmail: {email_address}\n\n{message_content}", "plain")
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_SENDER')
    msg['To'] = os.getenv('SMTP_RECEIVER')

    # SMTP server configuration and email sending logic
    try:
        with SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
            server.sendmail(os.getenv('SMTP_SENDER'), os.getenv('SMTP_RECEIVER'), msg.as_string())
        return "Email sent successfully!", False
    except SMTPConnectError:
        return "Failed to connect to the SMTP server.", True
    except SMTPAuthenticationError:
        return "SMTP authentication failed. Check your username and password.", True
    except SMTPRecipientsRefused:
        return "The recipient(s) was refused by the server.", True
    except SMTPSenderRefused:
        return "The sender was refused by the server.", True
    except SMTPDataError:
        return "The server replied with an unexpected error code.", True
    except Exception as e:
        return f"Unexpected error occurred while trying to send email: {str(e)}", True
