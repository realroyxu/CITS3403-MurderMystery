import unittest
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
from app.blueprints.post.post_db_helper import add_post
from datetime import datetime


class UserApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for all tests."""
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment after all tests."""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Set up before each test."""
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # user = User(username='testuser', password='testpassword')
        # db.session.add(user)
        # db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_success(self):
        username = "new"
        response = self.client.post('/api/register', json={
            'username': username,
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Account created for {username}!", response.get_json()['message'])

    def test_register_failure(self):
        response = self.client.post('/api/register', json={
            'username': 'aifert',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Error creating account', response.get_json()['message'])

    def test_login_success(self):
        response = self.client.post('/api/login', json={
            'username': 'aifert',
            'password': 'aaa'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_json()['message'])

    def test_login_failure(self):
        response = self.client.post('/api/login', json={
            'username': 'aifert',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Login Unsuccessful', response.get_json()['message'])

    def test_change_password_success(self):
        # Simulate a logged-in user
        with self.client.session_transaction() as sess:
            sess['userid'] = 'aifert'  # Assuming user ID 1 is 'testuser'

        response = self.client.post('/api/changepassword', json={
            'old_password': 'testpassword',
            'new_password': 'newtestpassword'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Password changed successfully', response.get_json()['message'])

    def test_change_password_success(self):
        with self.client.session_transaction() as sess:
            sess['userid'] = 1

        response = self.client.post('/api/changepassword', json={
            'old_password': 'www',
            'new_password': 'newtestpassword'
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn('Password changed successfully', response.get_json()['message'])

    def test_change_avatar_success(self):
        # Simulate a logged-in user
        with self.client.session_transaction() as sess:
            sess['userid'] = 1  # Assuming user ID 1 is 'testuser'

        response = self.client.post('/api/changeavatar', json={
            'avatar_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Avatar changed successfully', response.get_json()['message'])

    def test_change_avatar_invalid_request(self):
        response = self.client.post('/api/changeavatar', json={
            'avatar_id': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.get_json()['message'])

    def test_change_avatar_failure(self):
        # Simulate a logged-in user
        with self.client.session_transaction() as sess:
            sess['userid'] = 10

        # Assuming the service will fail due to some error
        response = self.client.post('/api/changeavatar', json={
            'avatar_id': 123
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error changing avatar', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
