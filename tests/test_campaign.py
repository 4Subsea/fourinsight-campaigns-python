from fourinsight.campaigns.campaign import BaseCampaign

import pytest


# @pytest.fixture
# def base_campaign(auth_session):
#     return BaseCampaign(auth_session, "1234")


class Test_BaseCampaign:
    def test_something(self, auth_session3):
        base_campaign = BaseCampaign(auth_session3, "1234")
