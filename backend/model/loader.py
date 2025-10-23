import torch


class ModelLoader:
    def __init__(self, onnx_file: str):
        self.__model = None
        pass

    @property
    def model(self):
        return self.__model


if __name__ == "__main__":
    raise ImportError("This is not main module")
