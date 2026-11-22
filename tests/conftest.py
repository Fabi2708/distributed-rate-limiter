import pytest
from app.main import storage

@pytest.fixture(autouse=True)
def reset_storage():
    storage.storage.clear()