import unittest
from app import app, db, Email

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client and database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database for next test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        # Test if index page loads successfully
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_send_email(self):
        # Test the email sending endpoint
        response = self.app.post('/send_email', data={
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email sent successfully!", response.data)

        # Verify the email was saved to the database
        with app.app_context():
            email = Email.query.first()
            self.assertIsNotNone(email)
            self.assertEqual(email.fname, 'John')
            self.assertEqual(email.lname, 'Doe')

    def test_get_emails(self):
        # First, add an email to the database
        email_entry = Email(fname='Jane', lname='Smith', email='jane.smith@example.com', subject='Hello', message='Hi there!')
        with app.app_context():
            db.session.add(email_entry)
            db.session.commit()

        # Fetch emails
        response = self.app.get('/emails')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['fname'], 'Jane')
        self.assertEqual(json_data[0]['lname'], 'Smith')

if __name__ == '__main__':
    unittest.main()