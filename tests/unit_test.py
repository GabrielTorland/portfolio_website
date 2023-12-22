import unittest
from app import app, db, Email
import redis
from constants import EMAIL_LIMIT
import os

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

    def test_send_email_limiter(self):
        self.redis_client = redis.from_url(os.getenv('REDIS_URL'))
        self.redis_client.flushdb() 
        # Send 100 emails
        responses = []
        for i in range(EMAIL_LIMIT):
            response = self.app.post('/send_email', data={
                'fname': 'John',
                'lname': 'Doe',
                'email': 'john.doe@example.com',
                'subject': 'Test',
                'message': 'This is a test message.'
            })
            responses.append(response)
        # Expect 200 OK for all requests
        self.assertListEqual([response.status_code for response in responses], [200] * 100)

        # Send one more email to test the rate limit
        response = self.app.post('/send_email', data={
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test',
            'message': 'This is a test message.'
        })
        # Expect a 429 error
        self.assertEqual(response.status_code, 429) 
        self.redis_client.flushdb() 

if __name__ == '__main__':
    unittest.main()