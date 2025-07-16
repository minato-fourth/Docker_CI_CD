#!/usr/bin/env python3
"""
Load testing configuration for Flask Docker CI/CD application using Locust.
Run with: locust -f locustfile.py --host=http://localhost:5000
"""

from locust import HttpUser, task, between
import json


class FlaskAppUser(HttpUser):
    """Simulates a user interacting with the Flask application."""
    
    # Wait between 1 and 3 seconds between requests
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts."""
        # Perform any setup here (e.g., login)
        pass
    
    @task(3)
    def test_home_endpoint(self):
        """Test the main home endpoint (higher weight)."""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('message') == 'Hello from Docker CI/CD!':
                        response.success()
                    else:
                        response.failure("Unexpected response content")
                except json.JSONDecodeError:
                    response.failure("Response is not valid JSON")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('status') == 'healthy':
                        response.success()
                    else:
                        response.failure("Health check failed")
                except json.JSONDecodeError:
                    response.failure("Health response is not valid JSON")
            else:
                response.failure(f"Health check returned {response.status_code}")
    
    @task(1)
    def test_info_endpoint(self):
        """Test the application info endpoint."""
        with self.client.get("/info", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'name' in data and 'version' in data:
                        response.success()
                    else:
                        response.failure("Missing required info fields")
                except json.JSONDecodeError:
                    response.failure("Info response is not valid JSON")
            else:
                response.failure(f"Info endpoint returned {response.status_code}")
    
    @task(1)
    def test_404_handling(self):
        """Test 404 error handling."""
        with self.client.get("/nonexistent", catch_response=True) as response:
            if response.status_code == 404:
                try:
                    data = response.json()
                    if data.get('error') == 'Not Found':
                        response.success()
                    else:
                        response.failure("Unexpected 404 response format")
                except json.JSONDecodeError:
                    response.failure("404 response is not valid JSON")
            else:
                response.failure(f"Expected 404, got {response.status_code}")


class AdminUser(HttpUser):
    """Simulates an admin user with different usage patterns."""
    
    wait_time = between(2, 5)
    weight = 1  # Lower weight than regular users
    
    @task
    def admin_health_checks(self):
        """Admin performs more frequent health checks."""
        endpoints = ["/health", "/info"]
        for endpoint in endpoints:
            self.client.get(endpoint)


# Custom load test scenarios
class HighLoadUser(HttpUser):
    """Simulates high-load scenarios."""
    
    wait_time = between(0.1, 0.5)  # Very fast requests
    weight = 1
    
    @task
    def rapid_requests(self):
        """Make rapid requests to test performance under load."""
        self.client.get("/")
        self.client.get("/health")
