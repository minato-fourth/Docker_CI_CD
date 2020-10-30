from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Docker CI/CD!',
        'status': 'success',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'flask-docker-cicd',
        'version': '1.0.0'
    })

@app.route('/info')
def app_info():
    return jsonify({
        'name': 'Flask Docker CI/CD Demo',
        'version': '1.0.0',
        'description': 'A simple Flask app demonstrating Docker containerization and CI/CD pipeline',
        'endpoints': {
            '/': 'Main welcome message',
            '/health': 'Health check endpoint',
            '/info': 'Application information'
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=app.config['DEBUG'])
