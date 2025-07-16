#!/usr/bin/env python3
"""
Comprehensive test suite for Flask Docker CI/CD Demo Application
Tests all endpoints and functionality using unittest framework.
"""

import unittest
import json
import os
import sys
from datetime import datetime

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class FlaskAppTestCase(unittest.TestCase):
    """Test cases for Flask application endpoints."""

    def setUp(self):
        """Set up test client and configuration."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Clean up after tests."""
        self.ctx.pop()

    def test_hello_endpoint(self):
        """Test the main hello endpoint."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Hello from Docker CI/CD!')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('timestamp', data)
        
        # Verify timestamp format
        try:
            datetime.fromisoformat(data['timestamp'])
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'flask-docker-cicd')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('timestamp', data)

    def test_info_endpoint(self):
        """Test the application info endpoint."""
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Flask Docker CI/CD Demo')
        self.assertEqual(data['version'], '1.0.0')
        self.assertIn('description', data)
        self.assertIn('endpoints', data)
        self.assertIn('environment', data)
        
        # Check endpoints documentation
        endpoints = data['endpoints']
        self.assertIn('/', endpoints)
        self.assertIn('/health', endpoints)
        self.assertIn('/info', endpoints)

    def test_404_error_handler(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not Found')
        self.assertEqual(data['status_code'], 404)
        self.assertIn('message', data)

    def test_json_content_type(self):
        """Test that all endpoints return JSON content type."""
        endpoints = ['/', '/health', '/info']
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.content_type, 'application/json')

    def test_response_structure(self):
        """Test that responses have consistent structure."""
        response = self.client.get('/')
        data = json.loads(response.data)
        
        # Check required fields
        required_fields = ['message', 'status', 'timestamp', 'version']
        for field in required_fields:
            self.assertIn(field, data)

    def test_health_check_response_time(self):
        """Test that health check responds quickly."""
        import time
        start_time = time.time()
        response = self.client.get('/health')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        # Health check should respond within 1 second
        self.assertLess(end_time - start_time, 1.0)

    def test_multiple_requests(self):
        """Test handling multiple concurrent requests."""
        responses = []
        for _ in range(10):
            response = self.client.get('/')
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Hello from Docker CI/CD!')


class FlaskAppConfigTestCase(unittest.TestCase):
    """Test cases for Flask application configuration."""

    def setUp(self):
        """Set up test environment."""
        self.app = app

    def test_app_configuration(self):
        """Test application configuration."""
        self.assertIsNotNone(self.app.config.get('SECRET_KEY'))
        self.assertIn('DEBUG', self.app.config)

    def test_environment_variables(self):
        """Test environment variable handling."""
        # Test default values
        self.assertEqual(self.app.config.get('SECRET_KEY', ''), 
                        os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
