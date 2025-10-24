import os
from typing import List, Optional, Tuple

import cv2
import numpy as np
import onnxruntime as ort


class ONNXModel:
    """
    Minimal ONNXRuntime loader that accepts an OpenCV-decoded image (numpy.ndarray).
    Assumes an MNIST-like model expecting NCHW with shape required by onnx model
    """

    def __init__(self, onnx_path: str):
        if not os.path.isabs(onnx_path):
            onnx_path = os.path.join(os.path.dirname(__file__), onnx_path)
        self.__session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        ipt = self.__session.get_inputs()[0]
        self.__input_name = ipt.name
        self.__output_name = self.__session.get_outputs()[0].name
        self.__input_shape = [int(x) if isinstance(x, (int, np.integer)) else None for x in ipt.shape]

    def __preprocess(self, src_image: np.ndarray) -> np.ndarray:
        """
        Convert OpenCV BGR/gray image -> numpy array suitable for ONNX:
          - convert to grayscale (1 channel)
          - resize to required shape
          - scale to [0,1] float32
          - return shape (1,1,H,W)
        """
        if src_image is None:
            raise ValueError("Empty image is none")

        if src_image.ndim == 3 and src_image.shape[2] == 3:
            gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = src_image

        h, w = self.__input_shape[2:]
        if gray.shape != (h, w):
            gray = cv2.resize(gray, (w, h), cv2.INTER_LINEAR)

        arr = gray.astype(np.float32) / 255.0
        if arr.ndim == 2:
            arr = arr[:, :, None]

        arr = np.transpose(arr, (2, 0, 1))
        arr = np.expand_dims(arr, axis=0)
        return arr.astype(np.float32)

    def infer(self, image: np.ndarray) -> Tuple[int, float] | Tuple[None, None]:
        """
        Run model on a single OpenCV-decoded image (np.ndarray).
        Returns (pred_index, confidence) or None on failure.
        """
        try:
            arr = self.__preprocess(image)
            outputs = self.__session.run([self.__output_name], {self.__input_name: arr})
            logits = outputs[0][0]
            exp = np.exp(logits - np.max(logits))
            probs = exp / exp.sum()
            idx = int(np.argmax(probs))
            return idx, float(probs[idx])
        except:
            return None, None


if __name__ == "__main__":
    raise ImportError("This is not main module")
