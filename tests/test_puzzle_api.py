import unittest
from dotenv import load_dotenv
from app import create_app, db
from app.models.puzzle import Puzzle
from app.models.post import Post
from app.models.user import User
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

class PuzzleApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for all tests."""
        logging.debug('Setting up class...')
        load_dotenv()
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment after all tests."""
        logging.debug('Tearing down class...')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Set up before each test."""
        logging.debug('Setting up test...')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # user = User(username='testuser', password='testpassword')
        # db.session.add(user)
        # db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        logging.debug('Tearing down test...')
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_puzzle(self):
        logging.debug('Running test_get_puzzle...')
        # Add sample puzzle to the database
        puzzle_data = {
            "userid": 1,
            "puzzledata": "Sample puzzle data from get puzzle",
            "puzzleanswer": "Answer",
            "category": "Sample category",
            "updatetime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        puzzle = Puzzle(**puzzle_data)
        with self.app.app_context():
            db.session.add(puzzle)
            db.session.commit()
            puzzle_id = puzzle.puzzleid

            response = self.client.post('/api/getpuzzle', json={"puzzleid": puzzle_id})
            self.assertEqual(response.status_code, 200)
            self.assertIn("puzzle", response.get_json())

    def test_add_puzzle(self):
        logging.debug('Running test_add_puzzle...')
        with self.client.session_transaction() as sess:
            sess['userid'] = 1  # Simulate a logged-in user

        puzzle_data = {
            "puzzledata": "New puzzle data",
            "category": "New category"
        }
        response = self.client.post('/api/addpuzzle', json=puzzle_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Puzzle added successfully")

if __name__ == '__main__':
    unittest.main()
