import pytest
from unittest.mock import Mock

@pytest.fixture
def auth_session():
    auth_session = Mock()
    return auth_session


class Test_BaseCampaign:
    def test_something(self, myfix):
        print(myfix)