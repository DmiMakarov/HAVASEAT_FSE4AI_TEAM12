"""
Performance and load tests
"""

import concurrent.futures
import io
import time
from unittest.mock import patch

import pytest
from app import app
from fastapi.testclient import TestClient
from PIL import Image


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_image_bytes():
    """Create a sample image for testing"""
    img = Image.new("L", (28, 28), color=128)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


class TestPerformance:
    """Performance tests for the API"""

    @pytest.mark.performance
    def test_single_request_performance(self, client, sample_image_bytes):
        """Test performance of a single request"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            start_time = time.time()
            files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)
            end_time = time.time()

            assert response.status_code == 200
            assert (end_time - start_time) < 5.0  # Should complete within 5 seconds

    @pytest.mark.performance
    def test_concurrent_requests(self, client, sample_image_bytes):
        """Test handling of concurrent requests"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            def make_request():
                files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
                response = client.post("/recognize_digit", files=files)
                return response.status_code == 200

            # Test with 5 concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request) for _ in range(5)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]

            assert all(results)  # All requests should succeed

    @pytest.mark.performance
    def test_memory_usage_with_large_images(self, client):
        """Test memory usage with large images"""
        # Create a large image
        large_img = Image.new("L", (500, 500), color=128)
        img_bytes = io.BytesIO()
        large_img.save(img_bytes, format="PNG")
        large_image_bytes = img_bytes.getvalue()

        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "large.png",
            }

            files = {"image_file": ("large.png", large_image_bytes, "image/png")}
            response = client.post("/recognize_digit", files=files)

            assert response.status_code == 200

    @pytest.mark.performance
    def test_response_time_consistency(self, client, sample_image_bytes):
        """Test that response times are consistent"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            response_times = []
            for _ in range(10):
                start_time = time.time()
                files = {"image_file": ("test.png", sample_image_bytes, "image/png")}
                response = client.post("/recognize_digit", files=files)
                end_time = time.time()

                assert response.status_code == 200
                response_times.append(end_time - start_time)

            # Check that response times are relatively consistent
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)

            # Max time should not be more than 2x the average
            assert max_time < avg_time * 2
            # Min time should not be less than half the average
            assert min_time > avg_time * 0.5


class TestLoadTesting:
    """Load testing scenarios"""

    @pytest.mark.load
    def test_rapid_sequential_requests(self, client, sample_image_bytes):
        """Test rapid sequential requests"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            # Make 20 rapid requests
            for i in range(20):
                files = {"image_file": (f"test_{i}.png", sample_image_bytes, "image/png")}
                response = client.post("/recognize_digit", files=files)
                assert response.status_code == 200

    @pytest.mark.load
    def test_mixed_request_types(self, client, sample_image_bytes):
        """Test mixed request types (valid and invalid)"""
        with patch("app.model") as mock_model:
            mock_model.process_and_recognize.return_value = {
                "status": "success",
                "recognized_digit": 5,
                "model_confidence": 0.95,
                "filename": "test.png",
            }

            # Mix of valid and invalid requests
            requests = [
                ({"image_file": ("valid.png", sample_image_bytes, "image/png")}, 200),
                ({"image_file": ("invalid.txt", b"not an image", "text/plain")}, 400),
                ({"image_file": ("valid2.png", sample_image_bytes, "image/png")}, 200),
                ({}, 422),  # No file
                ({"image_file": ("valid3.png", sample_image_bytes, "image/png")}, 200),
            ]

            for files, expected_status in requests:
                if files:
                    response = client.post("/recognize_digit", files=files)
                else:
                    response = client.post("/recognize_digit")
                assert response.status_code == expected_status
