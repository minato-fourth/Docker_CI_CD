.PHONY: help install test build run clean

help:
	@echo "Available commands:"
	@echo "  install     - Install Python dependencies"
	@echo "  test        - Run test suite"
	@echo "  build       - Build Docker image"
	@echo "  run         - Run application locally"
	@echo "  clean       - Clean up Docker resources"

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest tests/ -v

build:
	docker build -t flask-docker-cicd .

run:
	python3 app.py

clean:
	docker system prune -f
