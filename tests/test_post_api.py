import unittest
from dotenv import load_dotenv
from app import create_app, db
from app.models.post import Post
from app.blueprints.post.post_db_helper import add_post
from datetime import datetime

class PostApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for all tests."""
        load_dotenv()
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
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_post(self):
        # Add sample post to the database
        post_data = {
            "userid": 1,
            "title": "Sample Post",
            "content": "This is a sample post.",
            "posttime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "posttype": "Type1",
            "puzzleid": 1,
        }
        with self.app.app_context():
            post_id = add_post(Post, post_data)

            response = self.client.post('/api/getpost', json={"postid": post_id})
            self.assertEqual(response.status_code, 200)
            self.assertIn("postid", response.json)
            self.assertIn("title", response.json)
            self.assertIn("content", response.json)
            self.assertIn("puzzledata", response.json)
            self.assertIn("comments", response.json)

    # def test_add_post(self):
    #     with self.client.session_transaction() as sess:
    #         sess['userid'] = 1

    #     data = {
    #         "title": "New Post",
    #         "content": "This is a new post.",
    #         "characters": "Character details",
    #         "answer": "hello"
    #     }

    #     response = self.client.post('/api/addpost', data=data)
    #     self.assertEqual(response.status_code, 200)
    #     print(response.json)
    #     self.assertIn("message", response.json)
    #     self.assertIn("newpostid", response.json)
    #     self.assertIn("story", response.json)

    def test_delete_post(self):
        post_data = {
            "userid": 1,
            "title": "Sample Post",
            "content": "This is a sample post.",
            "posttime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "posttype": "Type1",
            "puzzleid": 1,
        }
        print(post_data)
        with self.app.app_context():
            post_id = add_post(Post, post_data)

            with self.client.session_transaction() as sess:
                sess['username'] = 'aifert'

            with self.app.app_context():  # Ensure the context is active when deleting
                response = self.client.post(f'/api/delete_post/{post_id}')
                self.assertEqual(response.status_code, 200)
                self.assertIn("message", response.json)

if __name__ == '__main__':
    unittest.main()
