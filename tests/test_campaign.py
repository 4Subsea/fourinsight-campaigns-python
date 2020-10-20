from fourinsight.campaigns.campaign import BaseCampaign

import pytest
from unittest.mock import Mock


@pytest.fixture
def BaseCampaign(auth_session):
    return Mock()


class Test_BaseCampaign:
    def test_something(self):
        1 == 1
