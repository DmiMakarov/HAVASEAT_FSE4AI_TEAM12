#!/bin/bash

# Startup script for Digit Recognition Application

set -e

echo "🚀 Starting Digit Recognition Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from env.example..."
    cp env.example .env
    echo "✅ Created .env file. Please review and update the configuration if needed."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Parse command line arguments
CMD=${1:-up}

if [ "$CMD" = "up" ] || [ "$CMD" = "start" ]; then
    echo "🛠️  Starting development environment..."
    docker-compose up --build
elif [ "$CMD" = "down" ] || [ "$CMD" = "stop" ]; then
    echo "🛑 Stopping all services..."
    docker-compose down
    echo "✅ All services stopped."
else
    echo "❌ Unknown command: $CMD"
    echo "Usage: ./start.sh [up|stop]"
    echo "  up   - Start development environment (default)"
    echo "  stop - Stop all services"
    exit 1
fi

