from fourinsight.campaigns.campaign import BaseCampaign


class Test_BaseCampaign:
    def test_something(self, auth_session2):
        base_campaign = BaseCampaign(auth_session2, "1234")
