import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app.api.models import setup_db, Region, Trail, Review
import config

TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imc2TktBSHp5b094TWRMNzRGcWlKNyJ9.eyJpc3MiOiJodHRwczovL3N0cnVkZXYtdG4uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGJmZjI4NGQ2ZTViMDA2Y2Y2OGNlNyIsImF1ZCI6Ikhpa2VUTkFQSSIsImlhdCI6MTYwODI2MjMwMiwiZXhwIjoxNjA4MjY5NTAyLCJhenAiOiJXNm5INnZLNXpnOVR2ZWVEWlFhQVA4dHliR3JFZVAzZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJlZ2lvbnMiLCJkZWxldGU6cmV2aWV3cyIsImRlbGV0ZTp0cmFpbHMiLCJnZXQ6cmV2aWV3cyIsInBhdGNoOnJlZ2lvbnMiLCJwYXRjaDpyZXZpZXdzIiwicGF0Y2g6dHJhaWxzIiwicG9zdDpyZWdpb25zIiwicG9zdDpyZXZpZXdzIiwicG9zdDp0cmFpbHMiXX0.UJjQUpjFEqf1ylupoMjB6xPamkosXM0nElwVYfVs5M8RRdVfAmhgyAK-4-_f3fUGeq7nDl7Ap8eOR8mfo-ThlEHs6zr0iwANu_4VyQwDjkfIHyE6foYXDSOIgOtqWa5xnJcG6OPbqgaBXIqWB-8RomgzjRQIWrAwj3Oer84VH3QGfMTzhb7MkbU3yUgNUvj0M11X3h7ZzYx_q_KM1ts3dHnSgPGjAidpz4UG0H87ABUn_yyM3uHZih_JC3sXFWltSmjKzG7HJiN9sVdubWBlQsPMpVsLskyhSQGRzT2kVT7nK9Or82yfQw9dQK29Pypsra0NjaB8iQhbnwUW6H-WLQ'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_user = 'postgres' #os.getenv('DB_USER')
        self.db_password = 'pgsql' #os.getenv('DB_PASSWORD')
        self.database_name = 'hiketn'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.db_user, self.db_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_review = {
            "rating": 4,
            "comment": "BlaBla",
            "trail_id": 4
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TESTS
    """
    def open_with_auth(self, url, method, token):
        return self.client().open(
            url,
            method=method,
            headers={
                'Authorization': 'Bearer {}'.format(token)
            }
        )
    
    def test_get_trails(self):
        res = self.client().get('/api/trails')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['trails']))
        self.assertTrue(data['total_trails'])
    
    def test_404_get_trails(self):
        res = self.client().get('/api/trails?page=30')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
    
    def test_get_regions(self):
        res = self.client().get('/api/regions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['regions']))
        self.assertTrue(data['total_regions'])

    def test_404_get_regions(self):
        res = self.client().get('/api/regions?page=30')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)

    def test_401_get_reviews_without_auth(self):
        res = self.client().get('/api/reviews')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_reviews_with_auth(self):
        res = self.open_with_auth('/api/reviews', 'GET', TOKEN)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['reviews']))
        self.assertTrue(data['total_reviews'])

    def test_delete_trail_with_auth(self):
        res = self.open_with_auth('/api/trails/9', 'DELETE', TOKEN)
        data = json.loads(res.data)

        trail = Trail.query.filter(Trail.id == 9).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 9)
        self.assertTrue(data['total_trails'])

    def test_404_delete_trail_fails(self):
        res = self.open_with_auth('/api/trails/900', 'DELETE', TOKEN)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_add_reviews_with_auth(self):
        res = self.client().post('/api/reviews', headers={'Authorization': 'Bearer {}'.format(TOKEN)}, json=self.new_review)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_reviews'])

    def test_update_review_with_auth(self):
        res = self.client().patch('/api/reviews/10', headers={'Authorization': 'Bearer {}'.format(TOKEN)}, json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

if __name__ == '__main__':
    unittest.main()