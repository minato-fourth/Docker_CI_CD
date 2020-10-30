import unittest
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_hello_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Hello from Docker CI/CD!')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('timestamp', data)

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'flask-docker-cicd')
        self.assertEqual(data['version'], '1.0.0')

    def test_info_endpoint(self):
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Flask Docker CI/CD Demo')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('description', data)
        self.assertIn('endpoints', data)

    def test_404_error_handler(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not Found')
        self.assertEqual(data['status_code'], 404)

if __name__ == '__main__':
    unittest.main()
