# Flask Docker CI/CD Pipeline

A DevOps project demonstrating containerization of a Flask web application with automated CI/CD pipeline using GitHub Actions.

## Features

- Flask Web Application with REST endpoints
- Docker containerization with production-ready configuration
- Automated CI/CD pipeline with GitHub Actions
- Unit testing with pytest
- Multi-container setup with Docker Compose

## Project Structure

```
├── .github/workflows/ci-cd.yml    # GitHub Actions CI/CD pipeline
├── tests/test_app.py               # Unit tests
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Production Docker image
├── docker-compose.yml              # Multi-container orchestration
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## Quick Start

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd Docker_CI_CD

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Docker

```bash
# Build and run
docker build -t flask-docker-cicd .
docker run -d -p 5000:5000 flask-docker-cicd

# Using Docker Compose
docker-compose up -d
```

### Testing

```bash
python -m pytest tests/ -v
```

## API Endpoints

- `GET /` - Main welcome message
- `GET /health` - Health check endpoint
- `GET /info` - Application information

## CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Runs tests on every push
2. Performs security scanning
3. Builds and pushes Docker images
4. Deploys to staging environment

### Required Secrets

Configure in GitHub repository settings:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token

## License

MIT License - see LICENSE file for details.
