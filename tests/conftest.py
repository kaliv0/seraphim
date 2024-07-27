import pytest
from src.api import API


@pytest.fixture
def api():
    return API(templates_dir="example/templates", static_dir="example/static")


@pytest.fixture
def client(api):
    return api.test_session()
