"""
Shared test fixtures and configuration
"""
import pytest
import numpy as np
from PIL import Image
import io


@pytest.fixture
def sample_digit_images():
    """Create sample digit images for testing"""
    images = {}

    # Create images for digits 0-9
    for digit in range(10):
        # Create a simple 28x28 grayscale image with the digit
        img = Image.new('L', (28, 28), color=0)  # Black background

        # Add some pattern to make it look like a digit
        pixels = np.array(img)
        # Add some white pixels in a pattern
        for i in range(5, 23):
            for j in range(5, 23):
                if (i + j + digit) % 3 == 0:
                    pixels[i, j] = 255

        img = Image.fromarray(pixels)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        images[f'digit_{digit}'] = img_bytes.getvalue()

    return images


@pytest.fixture
def corrupted_image_bytes():
    """Create corrupted image data for testing"""
    return b"corrupted image data that cannot be decoded"


@pytest.fixture
def large_image_bytes():
    """Create a large image for testing file size limits"""
    # Create a large image (1000x1000)
    img = Image.new('L', (1000, 1000), color=128)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()


@pytest.fixture
def empty_image_bytes():
    """Create empty image data"""
    return b""


@pytest.fixture
def non_image_bytes():
    """Create non-image file data"""
    return b"This is not an image file at all"


@pytest.fixture
def mock_model_response():
    """Mock model response for testing"""
    return {
        "status": "success",
        "recognized_digit": 5,
        "model_confidence": 0.95,
        "filename": "test.png"
    }


@pytest.fixture
def mock_model_error_response():
    """Mock model error response for testing"""
    return {
        "status": "error",
        "error": "Model inference failed"
    }
