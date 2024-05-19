import unittest
from app import create_app, db
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.models.puzzle import Puzzle
from datetime import datetime
import json

class CommentApiTestCase(unittest.TestCase):

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
        user = User(username='testuser4', password='testpassword')
        puzzle = Puzzle(userid=1, puzzledata="hello_world", updatetime=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), category="hello", puzzleanswer="hello")
        post = Post(userid=1, title='Sample Post', content='This is a sample post.', posttime=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), posttype='Type1', puzzleid=1)
        db.session.add(user)
        db.session.add(post)
        db.session.add(puzzle)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_comment(self):
        with self.client.session_transaction() as sess:
            sess['userid'] = 1

        comment_data = {
            "postid": 1,
            "userid": 1,
            "commenttext": "This is a test comment.",
            "commenttime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        response = self.client.post('/api/comment/1', json=comment_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Comment added successfully")

    def test_get_comment(self):
        comment_data = {
            "postid": 1,
            "userid": 1,
            "commenttext": "Sample comment",
            "commenttime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        comment = Comment(**comment_data)
        with self.app.app_context():
            db.session.add(comment)
            db.session.commit()

            response = self.client.post('/api/getcomment/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Comment get successfully")

if __name__ == '__main__':
    unittest.main()
