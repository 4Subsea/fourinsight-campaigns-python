import pytest
from unittest.mock import Mock


@pytest.fixture
def myfix():
    return "myfix-out"


@pytest.fixture
def response():
    response = Mock()
    return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session.get.return_value = response
    auth_session._api_base_url = "test"
    return auth_session
