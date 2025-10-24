from typing import Tuple

import numpy as np

from .onnx import ONNXModel as ONNX


class MNISTModel:
    """Simple mnist digit classifier that incapsulates ONNX model"""

    def __init__(self, *args, **kwargs):
        self.__onnx = ONNX("mnist-12.onnx")

    def recognize_digit(self, image: np.ndarray) -> tuple[int, float] | None:
        return self.__onnx.infer(image)


if __name__ == "__main__":
    raise ImportError("This is not main module")
