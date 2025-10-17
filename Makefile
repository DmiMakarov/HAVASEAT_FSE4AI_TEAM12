.PHONY: help up start stop restart logs clean build test test-watch test-ui test-coverage shell

# Default target
help:
	@echo "🎯 Digit Recognition Application - Docker Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make up            - Start development environment"
	@echo "  make start         - Start in background (detached)"
	@echo "  make stop          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - View logs (follow mode)"
	@echo "  make build         - Build containers"
	@echo "  make clean         - Clean up containers and volumes"
	@echo "  make shell         - Open shell in frontend container"
	@echo "  make test          - Run tests"
	@echo "  make test-watch    - Run tests in watch mode"
	@echo "  make test-ui       - Run tests with UI"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""

# Start development environment
up:
	@echo "🛠️  Starting development environment..."
	@if [ ! -f .env ]; then cp env.example .env; echo "✅ Created .env file"; fi
	docker-compose up

# Start in background
start:
	@echo "🛠️  Starting development environment (background)..."
	@if [ ! -f .env ]; then cp env.example .env; echo "✅ Created .env file"; fi
	docker-compose up -d

# Stop all services
stop:
	@echo "🛑 Stopping all services..."
	docker-compose down

# Restart services
restart:
	@echo "🔄 Restarting services..."
	docker-compose restart

# View logs
logs:
	@echo "📋 Viewing logs..."
	docker-compose logs -f

# View frontend logs
logs-frontend:
	docker-compose logs -f frontend

# View backend logs
logs-backend:
	docker-compose logs -f backend

# Build containers
build:
	@echo "🔨 Building containers..."
	docker-compose build

# Build with no cache
build-fresh:
	@echo "🔨 Building containers (no cache)..."
	docker-compose build --no-cache

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	@echo "✅ Cleanup complete"

# Open shell in frontend container
shell:
	@echo "🐚 Opening shell in frontend container..."
	docker-compose exec frontend sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	npm install

# Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose run --rm frontend npm test

# Run tests in watch mode
test-watch:
	@echo "🧪 Running tests in watch mode..."
	docker-compose run --rm frontend npm test -- --watch

# Run tests with UI
test-ui:
	@echo "🧪 Running tests with UI..."
	docker-compose run --rm -p 51204:51204 frontend npm run test:ui -- --host

# Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	docker-compose run --rm frontend npm run test:coverage

# Check status
status:
	@echo "📊 Container status:"
	docker-compose ps

# Show container resource usage
stats:
	@echo "📈 Resource usage:"
	docker stats --no-stream

