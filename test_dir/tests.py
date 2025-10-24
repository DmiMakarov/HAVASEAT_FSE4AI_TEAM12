from fastapi.testclient import TestClient
import pytest
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from app import app  # Replace 'app' with the actual module name

client = TestClient(app)

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Digit Recognition API is running"}

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def create_test_image():
    """Helper function to create a test image."""
    img = np.zeros((28, 28, 3), dtype=np.uint8)
    img.fill(255)  # Fill with white color
    return img

def test_recognize_digit():
    """Test the recognize_digit endpoint with a valid image."""
    test_image = create_test_image()

    # Convert the image to bytes
    is_success, encoded_image = cv2.imencode('.png', test_image)
    assert is_success, "Could not encode image"

    image_bytes = encoded_image.tobytes()

    # Send a POST request with the image
    response = client.post("/recognize_digit", files={"image_file": ("test_image.png", image_bytes, "image/png")})

    # Check the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["recognized_digit"] == 7
    assert response_data["model_confidence"] == 0.95
    assert response_data["filename"] == "test_image.png"

def test_recognize_digit_invalid_file():
    """Test the recognize_digit endpoint with an invalid file."""
    response = client.post("/recognize_digit", files={"image_file": ("test_file.txt", b"not an image", "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"detail": "File must be an image"}

def test_recognize_digit_empty_image():
    """Test the recognize_digit endpoint with an empty image."""
    empty_image = np.zeros((0, 0), dtype=np.uint8)
    is_success, encoded_image = cv2.imencode('.png', empty_image)
    assert is_success, "Could not encode image"

    image_bytes = encoded_image.tobytes()

    response = client.post("/recognize_digit", files={"image_file": ("empty_image.png", image_bytes, "image/png")})
    assert response.status_code == 500
    assert "Error processing image" in response.json()["detail"]

def test_recognize_digit_model_error():
    """Test the recognize_digit endpoint with a model error."""
    # Override the mock to return None values
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(model, "recognize_digit", lambda x: (None, None))
        test_image = create_test_image()
        is_success, encoded_image = cv2.imencode('.png', test_image)
        assert is_success, "Could not encode image"

        image_bytes = encoded_image.tobytes()

        response = client.post("/recognize_digit", files={"image_file": ("test_image.png", image_bytes, "image/png")})
        assert response.status_code == 500
        assert response.json()["detail"] == "Model inference error"

