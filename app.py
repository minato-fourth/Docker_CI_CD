#!/usr/bin/env python3
"""
Flask Web Application for Docker CI/CD Pipeline Demo
A simple web application demonstrating containerization and CI/CD practices.
"""

from flask import Flask, jsonify
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def hello():
    """Main endpoint returning a welcome message."""
    message = {
        'message': 'Hello from Docker CI/CD!',
        'status': 'success',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
    logger.info(f"Hello endpoint accessed at {message['timestamp']}")
    return jsonify(message)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'flask-docker-cicd',
        'version': '1.0.0'
    }
    return jsonify(health_status)

@app.route('/info')
def app_info():
    """Application information endpoint."""
    info = {
        'name': 'Flask Docker CI/CD Demo',
        'version': '1.0.0',
        'description': 'A simple Flask app demonstrating Docker containerization and CI/CD pipeline',
        'endpoints': {
            '/': 'Main welcome message',
            '/health': 'Health check endpoint',
            '/info': 'Application information'
        },
        'environment': {
            'python_version': os.sys.version,
            'flask_debug': app.config['DEBUG']
        }
    }
    return jsonify(info)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Flask application on {host}:{port}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )
