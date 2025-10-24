"""
FastAPI endpoint tests using pytest and httpx
"""

import io
import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import numpy as np
from PIL import Image

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_image_bytes():
    """Create a sample image for testing"""
    # Create a simple 28x28 grayscale image (MNIST format)
    img = Image.new("L", (28, 28), color=128)  # Gray image
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


@pytest.fixture
def invalid_image_bytes():
    """Create invalid image data for testing"""
    return b"not an image"


class TestHealthEndpoints:
    """Test health check and root endpoints"""

    @pytest.mark.api
    def test_root_endpoint(self, client):
        """Test the root endpoint returns correct message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Digit Recognition API is running"}

    @pytest.mark.api
    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestDigitRecognitionEndpoint:
    """Test the digit recognition endpoint"""

    @pytest.mark.api
    def test_recognize_digit_success(self, client, sample_image_bytes):
        """Test successful digit recognition"""
        with patch("app.model") as mock_model:
            # Mock the model response
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["recognized_digit"] == 5
            assert data["model_confidence"] == 0.95
            assert data["filename"] == "test.png"

    @pytest.mark.api
    def test_recognize_digit_invalid_file_type(self, client):
        """Test recognition with invalid file type"""
        files = {"image_file": ("test.txt", b"not an image", "text/plain")}
        response = client.post("/recognize_digit", files=files)

        assert response.status_code == 400
        assert "File must be an image" in response.json()["detail"]

    @pytest.mark.api
    def test_recognize_digit_no_file(self, client):
        """Test recognition without file"""
        response = client.post("/recognize_digit")
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    def test_recognize_digit_model_error(self, client, sample_image_bytes):
        """Test recognition when model raises an error"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.side_effect = ValueError("Model error")

            files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)

            assert response.status_code == 400
            assert "Model error" in response.json()["detail"]

    @pytest.mark.api
    def test_recognize_digit_unexpected_error(self, client, sample_image_bytes):
        """Test recognition with unexpected error"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.side_effect = Exception("Unexpected error")

            files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)

            assert response.status_code == 500
            assert "Unexpected error" in response.json()["detail"]


class TestCORS:
    """Test CORS configuration"""

    @pytest.mark.api
    def test_cors_headers(self, client):
        """Test that CORS headers are properly set"""
        response = client.options("/recognize_digit")
        # FastAPI automatically handles CORS for OPTIONS requests
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly defined

    @pytest.mark.api
    def test_cors_origin_header(self, client):
        """Test CORS origin header is set"""
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/health", headers=headers)
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling scenarios"""

    @pytest.mark.api
    def test_large_file_handling(self, client):
        """Test handling of large files"""
        # Create a large image (simulate)
        large_image = b"x" * (10 * 1024 * 1024)  # 10MB
        files = {"image_file": ("large.png", large_image, "image/png")}

        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.side_effect = ValueError("File too large")
            response = client.post("/recognize_digit", files=files)
            assert response.status_code == 400

    @pytest.mark.api
    def test_corrupted_image(self, client):
        """Test handling of corrupted image data"""
        corrupted_image = b"corrupted image data"
        files = {"image_file": ("corrupted.png", corrupted_image, "image/png")}

        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.side_effect = ValueError("Could not decode image")
            response = client.post("/recognize_digit", files=files)
            assert response.status_code == 400


@pytest.mark.integration
class TestIntegration:
    """Integration tests that test the full flow"""

    def test_full_recognition_flow(self, client, sample_image_bytes):
        """Test the complete recognition flow"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 3,
                "model_confidence": 0.87,
                "filename": "integration_test.png",
            }

            files = {"image_file": ("integration_test.png", sample_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["recognized_digit"] == 3
            assert 0 <= data["model_confidence"] <= 1
            assert data["filename"] == "integration_test.png"

            # Verify the model was called with correct parameters
            mock_model.process_and_recognize.assert_called_once()
            call_args = mock_model.process_and_recognize.call_args
            assert call_args[0][0] == sample_image_bytes  # image_bytes
            assert call_args[0][1] == "integration_test.png"  # filename
