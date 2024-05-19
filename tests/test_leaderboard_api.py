import unittest
from app import create_app, db
from app.models.user import User
from app.models.siteleaderboard import SiteLeaderboard
from app.models.postleaderboard import PostLeaderboard
from datetime import datetime
import json

class LeaderboardApiTestCase(unittest.TestCase):

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
        user1 = User(username='testuser', password='testpassword')
        user2 = User(username='testuser2', password='testpassword')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_siteleaderboard_postcount_order(self):
        slb_data = [
            {"userid": 1, "postcount": 10, "solvecount": 5},
            {"userid": 2, "postcount": 20, "solvecount": 15}
        ]
        with self.app.app_context():
            for entry in slb_data:
                slb_entry = SiteLeaderboard(**entry)
                db.session.add(slb_entry)
            db.session.commit()

            response = self.client.get('/api/getslbbypost?limit=2')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['username'], 'testuser')

    def test_get_siteleaderboard_solvecount_order(self):
        slb_data = [
            {"userid": 1, "postcount": 10, "solvecount": 5},
            {"userid": 2, "postcount": 20, "solvecount": 15}
        ]
        with self.app.app_context():
            for entry in slb_data:
                slb_entry = SiteLeaderboard(**entry)
                db.session.add(slb_entry)
            db.session.commit()

            response = self.client.get('/api/getslbbysolve?limit=2')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['username'], 'testuser')

if __name__ == '__main__':
    unittest.main()
