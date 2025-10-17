#!/bin/bash

# Test runner script for Digit Recognition Application

set -e

echo "🧪 Digit Recognition - Test Suite"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the project root"
    exit 1
fi

# Parse command line arguments
MODE=${1:-standard}

case $MODE in
    "standard"|"test")
        echo "🏃 Running standard tests..."
        docker-compose run --rm frontend npm test
        ;;

    "watch")
        echo "👀 Running tests in watch mode..."
        echo "Press Ctrl+C to exit"
        docker-compose run --rm frontend npm test -- --watch
        ;;

    "ui")
        echo "🎨 Starting test UI..."
        echo "Access the UI at: http://localhost:51204"
        docker-compose run --rm -p 51204:51204 frontend npm run test:ui -- --host
        ;;

    "coverage")
        echo "📊 Running tests with coverage..."
        docker-compose run --rm frontend npm run test:coverage
        echo ""
        echo "✅ Coverage report generated!"
        echo "View HTML report: frontend/coverage/index.html"
        ;;

    "local")
        echo "💻 Running tests locally (without Docker)..."
        cd frontend
        npm test
        cd ..
        ;;

    "local-coverage")
        echo "💻 Running tests locally with coverage..."
        cd frontend
        npm run test:coverage
        echo ""
        echo "✅ Coverage report generated!"
        echo "View HTML report: frontend/coverage/index.html"
        cd ..
        ;;

    "ci")
        echo "🤖 Running tests in CI mode..."
        docker-compose run --rm frontend npm test -- --run --reporter=verbose
        echo ""
        echo "✅ All tests passed!"
        ;;

    "help"|"-h"|"--help")
        echo "Usage: ./run-tests.sh [mode]"
        echo ""
        echo "Available modes:"
        echo "  standard (default) - Run all tests once"
        echo "  watch              - Run tests in watch mode"
        echo "  ui                 - Run tests with interactive UI"
        echo "  coverage           - Run tests with coverage report"
        echo "  local              - Run tests locally without Docker"
        echo "  local-coverage     - Run tests locally with coverage"
        echo "  ci                 - Run tests in CI mode"
        echo "  help               - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run-tests.sh              # Run standard tests"
        echo "  ./run-tests.sh watch        # Watch mode"
        echo "  ./run-tests.sh coverage     # With coverage"
        echo ""
        exit 0
        ;;

    *)
        echo "❌ Unknown mode: $MODE"
        echo "Run './run-tests.sh help' for available modes"
        exit 1
        ;;
esac

echo ""
echo "✨ Test execution completed!"

