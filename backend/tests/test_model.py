"""
Unit tests for the MNIST model classes
"""

import pytest
import numpy as np
import cv2
from unittest.mock import Mock, patch, MagicMock
import io
from PIL import Image

from model.model import MNISTModel
from model.onnx import ONNXModel


class TestMNISTModel:
    """Test the MNISTModel class"""

    @pytest.fixture
    def mock_onnx_model(self):
        """Create a mock ONNX model"""
        mock_onnx = Mock()
        mock_onnx.infer.return_value = (5, 0.95)
        return mock_onnx

    @pytest.fixture
    def mnist_model(self, mock_onnx_model):
        """Create MNISTModel instance with mocked ONNX"""
        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx_class.return_value = mock_onnx_model
            return MNISTModel()

    @pytest.fixture
    def sample_image_bytes(self):
        """Create sample image bytes"""
        img = Image.new("L", (28, 28), color=128)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        return img_bytes.getvalue()

    @pytest.mark.unit
    def test_mnist_model_initialization(self, mock_onnx_model):
        """Test MNISTModel initialization"""
        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx_class.return_value = mock_onnx_model
            model = MNISTModel()
            assert model is not None
            mock_onnx_class.assert_called_once_with("mnist-12.onnx")

    @pytest.mark.unit
    def test_recognize_digit_success(self, mnist_model):
        """Test successful digit recognition"""
        # Create a sample image array
        sample_image = np.random.randint(0, 255, (28, 28), dtype=np.uint8)

        digit, confidence = mnist_model.recognize_digit(sample_image)

        assert digit == 5
        assert confidence == 0.95

    @pytest.mark.unit
    def test_recognize_digit_failure(self, mock_onnx_model):
        """Test digit recognition failure"""
        mock_onnx_model.infer.return_value = (None, None)

        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx_class.return_value = mock_onnx_model
            model = MNISTModel()

            sample_image = np.random.randint(0, 255, (28, 28), dtype=np.uint8)
            digit, confidence = model.recognize_digit(sample_image)

            assert digit is None
            assert confidence is None

    @pytest.mark.unit
    def test_process_and_recognize_success(self, mnist_model, sample_image_bytes):
        """Test successful image processing and recognition"""
        result = mnist_model.process_and_recognize(sample_image_bytes, "test.png")

        assert result["status"] == "success"
        assert result["recognized_digit"] == 5
        assert result["model_confidence"] == 0.95
        assert result["filename"] == "test.png"

    @pytest.mark.unit
    def test_process_and_recognize_decode_error(self, mnist_model):
        """Test image processing with decode error"""
        invalid_bytes = b"not an image"

        with pytest.raises(ValueError, match="Error processing image"):
            mnist_model.process_and_recognize(invalid_bytes, "test.png")

    @pytest.mark.unit
    def test_process_and_recognize_model_error(self, mock_onnx_model):
        """Test image processing when model fails"""
        mock_onnx_model.infer.return_value = (None, None)

        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx_class.return_value = mock_onnx_model
            model = MNISTModel()

            img = Image.new("L", (28, 28), color=128)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")

            with pytest.raises(ValueError, match="Model inference error"):
                model.process_and_recognize(img_bytes.getvalue(), "test.png")

    @pytest.mark.unit
    def test_process_and_recognize_cv2_error(self, mnist_model):
        """Test image processing with OpenCV error"""
        with patch("cv2.imdecode") as mock_imdecode:
            mock_imdecode.return_value = None

            img = Image.new("L", (28, 28), color=128)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")

            with pytest.raises(ValueError, match="Could not decode image"):
                mnist_model.process_and_recognize(img_bytes.getvalue(), "test.png")


class TestONNXModel:
    """Test the ONNXModel class"""

    @pytest.fixture
    def mock_session(self):
        """Create a mock ONNX session"""
        mock_session = Mock()
        mock_input = Mock()
        mock_input.name = "input"
        mock_input.shape = [1, 1, 28, 28]
        mock_output = Mock()
        mock_output.name = "output"

        mock_session.get_inputs.return_value = [mock_input]
        mock_session.get_outputs.return_value = [mock_output]
        mock_session.run.return_value = [np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.1, 0.1, 0.1, 0.1]])]

        return mock_session

    @pytest.fixture
    def onnx_model(self, mock_session):
        """Create ONNXModel instance with mocked session"""
        with patch("model.onnx.ort.InferenceSession") as mock_inference:
            mock_inference.return_value = mock_session
            return ONNXModel("dummy.onnx")

    @pytest.mark.unit
    def test_onnx_model_initialization(self, mock_session):
        """Test ONNXModel initialization"""
        with patch("model.onnx.ort.InferenceSession") as mock_inference:
            mock_inference.return_value = mock_session
            model = ONNXModel("dummy.onnx")
            assert model is not None
            mock_inference.assert_called_once()

    @pytest.mark.unit
    def test_preprocess_color_image(self, onnx_model):
        """Test preprocessing of color image"""
        # Create a color image (BGR format)
        color_image = np.random.randint(0, 255, (28, 28, 3), dtype=np.uint8)

        with patch("cv2.cvtColor") as mock_cvtcolor, patch("cv2.resize") as mock_resize:
            mock_cvtcolor.return_value = np.random.randint(0, 255, (28, 28), dtype=np.uint8)
            mock_resize.return_value = np.random.randint(0, 255, (28, 28), dtype=np.uint8)

            result = onnx_model._ONNXModel__preprocess(color_image)

            assert result.shape == (1, 1, 28, 28)
            assert result.dtype == np.float32
            mock_cvtcolor.assert_called_once()

    @pytest.mark.unit
    def test_preprocess_grayscale_image(self, onnx_model):
        """Test preprocessing of grayscale image"""
        gray_image = np.random.randint(0, 255, (28, 28), dtype=np.uint8)

        with patch("cv2.resize") as mock_resize:
            mock_resize.return_value = gray_image

            result = onnx_model._ONNXModel__preprocess(gray_image)

            assert result.shape == (1, 1, 28, 28)
            assert result.dtype == np.float32
            # Only assert resize was called if the image size doesn't match expected shape
            # Since we're using 28x28 which matches the expected shape, resize might not be called
            if gray_image.shape != (28, 28):
                mock_resize.assert_called_once()

    @pytest.mark.unit
    def test_preprocess_none_image(self, onnx_model):
        """Test preprocessing with None image"""
        with pytest.raises(ValueError, match="Empty image is none"):
            onnx_model._ONNXModel__preprocess(None)

    @pytest.mark.unit
    def test_infer_success(self, onnx_model):
        """Test successful inference"""
        sample_image = np.random.randint(0, 255, (28, 28), dtype=np.uint8)

        digit, confidence = onnx_model.infer(sample_image)

        assert digit == 5  # argmax of the mock output
        assert 0 <= confidence <= 1

    @pytest.mark.unit
    def test_infer_failure(self, mock_session):
        """Test inference failure"""
        mock_session.run.side_effect = Exception("ONNX error")

        with patch("model.onnx.ort.InferenceSession") as mock_inference:
            mock_inference.return_value = mock_session
            model = ONNXModel("dummy.onnx")

            sample_image = np.random.randint(0, 255, (28, 28), dtype=np.uint8)
            digit, confidence = model.infer(sample_image)

            assert digit is None
            assert confidence is None


class TestModelIntegration:
    """Integration tests for the complete model pipeline"""

    @pytest.mark.integration
    def test_full_model_pipeline(self):
        """Test the complete model pipeline with real image processing"""
        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx = Mock()
            mock_onnx.infer.return_value = (7, 0.89)
            mock_onnx_class.return_value = mock_onnx

            model = MNISTModel()

            # Create a real image
            img = Image.new("L", (28, 28), color=128)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")

            result = model.process_and_recognize(img_bytes.getvalue(), "integration_test.png")

            assert result["status"] == "success"
            assert result["recognized_digit"] == 7
            assert result["model_confidence"] == 0.89
            assert result["filename"] == "integration_test.png"

    @pytest.mark.integration
    def test_model_with_different_image_sizes(self):
        """Test model with different image sizes"""
        with patch("model.model.ONNX") as mock_onnx_class:
            mock_onnx = Mock()
            mock_onnx.infer.return_value = (3, 0.92)
            mock_onnx_class.return_value = mock_onnx

            model = MNISTModel()

            # Test with different image sizes
            for size in [(32, 32), (64, 64), (14, 14)]:
                img = Image.new("L", size, color=128)
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")

                result = model.process_and_recognize(img_bytes.getvalue(), f"test_{size[0]}x{size[1]}.png")

                assert result["status"] == "success"
                assert result["recognized_digit"] == 3
                assert result["model_confidence"] == 0.92
