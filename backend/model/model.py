from loader import ModelLoader as Loader
from numpy.typing import NDArray


class MNISTModel:
    def __init__(self, *args, **kwargs):
        self.loader = Loader("mnist-12.onnx")
        pass

    def recognize_digit(self, image: NDArray) -> int | None:
        model = self.loader.model
        return model.infer(image)


if __name__ == "__main__":
    raise ImportError("This is not main module")
