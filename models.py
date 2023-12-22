from config import db
from datetime import datetime

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'date_sent': self.date_sent.strftime('%Y-%m-%d %H:%M:%S')
        }