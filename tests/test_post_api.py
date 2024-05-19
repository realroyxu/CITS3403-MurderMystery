import unittest
import json
import os
import io
from dotenv import load_dotenv
from app import db
from app.models.post import Post
from app import create_app
from app.blueprints.post import post_api_bp

class PostApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for all tests."""
        load_dotenv()
        cls.app = create_app('')  # Ensure create_app uses TestingConfig for 'testing'
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
        self.client = self.app.test_client()
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
            "title": "Sample Post",
            "content": "This is a sample post.",
            "userid": 1,
            "puzzleid": 1
        }
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()

        post_id = post.postid

        response = self.client.post('/api/getpost', json={"postid": post_id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("postid", response.json)
        self.assertIn("title", response.json)
        self.assertIn("content", response.json)
        self.assertIn("puzzledata", response.json)
        self.assertIn("comments", response.json)

    def test_add_post(self):
        with self.client.session_transaction() as sess:
            sess['userid'] = 1

        data = {
            "title": "New Post",
            "content": "This is a new post.",
            "characters": "Character details"
        }

        response = self.client.post('/api/addpost', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertIn("newpostid", response.json)
        self.assertIn("story", response.json)

    def test_edit_post(self):
        # Add sample post to the database
        post_data = {
            "title": "Sample Post",
            "content": "This is a sample post.",
            "userid": 1,
            "puzzleid": 1
        }
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()

        post_id = post.postid

        edit_data = {
            "postid": post_id,
            "title": "Edited Post",
            "content": "This post has been edited."
        }

        response = self.client.post('/api/editpost', json=edit_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

    def test_upload_image(self):
        # Add sample post to the database
        post_data = {
            "title": "Sample Post",
            "content": "This is a sample post.",
            "userid": 1,
            "puzzleid": 1
        }
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()

        post_id = post.postid

        with self.client.session_transaction() as sess:
            sess['userid'] = 1

        data = {
            'file': (io.BytesIO(b"abcdef"), 'test.png')
        }

        response = self.client.post(f'/api/uploadimage/{post_id}', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

    def test_delete_post(self):
        # Add sample post to the database
        post_data = {
            "title": "Sample Post",
            "content": "This is a sample post.",
            "userid": 1,
            "puzzleid": 1
        }
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()

        post_id = post.postid

        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'

        response = self.client.post(f'/api/delete_post/{post_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)


if __name__ == '__main__':
    unittest.main()
