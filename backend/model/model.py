from typing import Tuple

import cv2
import numpy as np

from .onnx import ONNXModel as ONNX


class MNISTModel:
    """Simple mnist digit classifier that incapsulates ONNX model"""

    def __init__(self, *args, **kwargs):
        self.__onnx = ONNX("mnist-12.onnx")

    def recognize_digit(self, image: np.ndarray) -> tuple[int, float] | None:
        return self.__onnx.infer(image)

    def process_and_recognize(self, image_bytes: bytes, filename: str) -> dict:
        """
        Process image bytes and recognize digit

        Args:
            image_bytes: Raw image data
            filename: Name of the uploaded file

        Returns:
            Dictionary with recognition results

        Raises:
            ValueError: If image cannot be decoded or model inference fails
        """
        try:
            # Decode image from bytes
            nparr = np.frombuffer(image_bytes, np.uint8)
            if nparr is None:
                raise ValueError("Could not decode image")

            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Could not decode image")

            # Get model prediction
            digit, confidence = self.recognize_digit(image)
            if digit is None or confidence is None:
                raise ValueError("Model inference error")

            return {
                "status": "success",
                "recognized_digit": digit,
                "model_confidence": round(confidence, 3),
                "filename": filename,
            }

        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")


if __name__ == "__main__":
    raise ImportError("This is not main module")
