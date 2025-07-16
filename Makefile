# Makefile for Flask Docker CI/CD Project
# Provides convenient commands for development and deployment

.PHONY: help install test build run clean deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install Python dependencies"
	@echo "  test        - Run test suite"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run code linting"
	@echo "  build       - Build Docker image"
	@echo "  run         - Run application locally"
	@echo "  docker-run  - Run application in Docker"
	@echo "  compose-up  - Start all services with Docker Compose"
	@echo "  compose-dev - Start development environment"
	@echo "  compose-down - Stop all services"
	@echo "  clean       - Clean up Docker resources"
	@echo "  deploy      - Deploy to production"
	@echo "  logs        - View application logs"

# Python environment setup
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Testing
test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 app.py tests/ --max-line-length=127
	bandit -r . -f json -o bandit-report.json || true

# Docker operations
build:
	docker build -t flask-docker-cicd .

run:
	python app.py

docker-run:
	docker run -d -p 5000:5000 --name flask-app flask-docker-cicd

# Docker Compose operations
compose-up:
	docker-compose up -d

compose-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

compose-down:
	docker-compose down

# Utility commands
clean:
	docker system prune -f
	docker-compose down -v --remove-orphans

deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.yml up -d --build

logs:
	docker-compose logs -f web

# Health check
health:
	curl -f http://localhost:5000/health || echo "Application not responding"

# Development helpers
dev-setup: install
	cp .env.example .env
	@echo "Development environment setup complete!"
	@echo "Edit .env file with your configuration"

# Security scan
security:
	safety check -r requirements.txt
	bandit -r . -f json -o bandit-report.json

# Database operations
db-init:
	docker-compose exec db psql -U flask_user -d flask_app -f /docker-entrypoint-initdb.d/init.sql

# Monitoring
monitor:
	@echo "Opening monitoring dashboards..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
