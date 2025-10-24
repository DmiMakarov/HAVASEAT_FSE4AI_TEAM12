import pytest
from unittest.mock import MagicMock
from app import app, model  # Replace 'app' with the actual module name

@pytest.fixture(autouse=True)
def mock_model(monkeypatch):
    mock_recognize_digit = MagicMock(return_value=(7, 0.95))
    monkeypatch.setattr(model, "recognize_digit", mock_recognize_digit)

