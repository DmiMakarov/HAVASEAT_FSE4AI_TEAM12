# Backend Tests

This directory contains comprehensive tests for the FastAPI backend application.

## Test Structure

- `test_api.py` - FastAPI endpoint tests
- `test_model.py` - Unit tests for MNIST model classes
- `test_performance.py` - Performance and load tests
- `test_conftest.py` - Shared test fixtures
- `pictures/` - Test images for digit recognition

## Running Tests

### Run all tests:
```bash
cd backend
python -m pytest tests/ -v
```

### Run specific test categories:
```bash
# Unit tests only
python -m pytest tests/ -v -m unit

# API tests only
python -m pytest tests/ -v -m api

# Integration tests only
python -m pytest tests/ -v -m integration

# Performance tests only
python -m pytest tests/ -v -m performance
```

### Run with coverage:
```bash
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and classes
- Mock external dependencies
- Fast execution

### API Tests (`@pytest.mark.api`)
- Test FastAPI endpoints
- Test request/response handling
- Test error scenarios

### Integration Tests (`@pytest.mark.integration`)
- Test complete workflows
- Test component interactions
- Test real data flow

### Performance Tests (`@pytest.mark.performance`)
- Test response times
- Test concurrent requests
- Test memory usage

### Load Tests (`@pytest.mark.load`)
- Test under high load
- Test resource limits
- Test stability

## Test Fixtures

The `test_conftest.py` file provides shared fixtures:
- `sample_digit_images` - Test images for digits 0-9
- `corrupted_image_bytes` - Invalid image data
- `large_image_bytes` - Large images for size testing
- `mock_model_response` - Mock model responses

## Dependencies

Required packages for testing:
- `pytest` - Test framework
- `httpx` - HTTP client for API testing
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting (optional)

## Configuration

Tests are configured via `pytest.ini`:
- Test discovery patterns
- Markers for test categorization
- Output formatting
- Async mode configuration
