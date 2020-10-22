import fourinsight.campaigns

import pytest


@pytest.fixture
def campaigns_api(auth_session):
    return fourinsight.campaigns.api.CampaignsAPI(auth_session)


class Test_CampaignsAPI:
    def test_init(self, campaigns_api, auth_session):
        assert campaigns_api._auth_session == auth_session

    def test_get_base_url(self, campaigns_api):
        assert campaigns_api._get_base_url() == "test_url"

    def test__get(self, campaigns_api, response):
        assert campaigns_api._get("test") == response
        response.raise_for_status.assert_called_once()

    def test_verify_type(self, campaigns_api):
        assert campaigns_api._verify_type("SWIM Campaign") == "SWIM Campaign"
        assert campaigns_api._verify_type("Campaign") == "Campaign"

    def test_verify_type_raises(self, campaigns_api):
        with pytest.raises(ValueError):
            campaigns_api._verify_type("test")

    def test_get_campaigns(self, campaigns_api, auth_session, response):
        campaigns_api.get_campaigns()
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_swim_campaigns(self, campaigns_api, auth_session, response):
        campaigns_api._get_swim_campaigns()
        auth_session.get.assert_called_once_with(
            "test_url/v1.0/Campaigns/Type/SWIM Campaign"
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_generic_campaigns(self, campaigns_api, auth_session, response):
        campaigns_api._get_generic_campaigns()
        auth_session.get.assert_called_once_with(
            "test_url/v1.0/Campaigns/Type/Campaign"
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_campaigns_swim(self, campaigns_api, auth_session, response):
        campaigns_api.get_campaigns(campaign_type="SWIM Campaign")
        auth_session.get.assert_called_once_with(
            "test_url/v1.0/Campaigns/Type/SWIM Campaign"
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_campaigns_generic(self, campaigns_api, auth_session, response):
        campaigns_api.get_campaigns(campaign_type="Campaign")
        auth_session.get.assert_called_once_with(
            "test_url/v1.0/Campaigns/Type/Campaign"
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_campaigns_raises(self, campaigns_api):
        with pytest.raises(ValueError):
            campaigns_api.get_campaigns(campaign_type="invalid_type")

    def test_get_campaign(self, campaigns_api, auth_session, response):
        campaigns_api.get_campaign("1234")
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns/1234")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_events(self, campaigns_api, auth_session, response):
        campaigns_api.get_events("1234")
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns/1234/Events")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_sensors(self, campaigns_api, auth_session, response):
        campaigns_api.get_sensors("1234")
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns/1234/Sensors")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_lowerstack(self, campaigns_api, auth_session, response):
        campaigns_api.get_lowerstack("1234")
        auth_session.get.assert_called_once_with(
            "test_url/v1.0/Campaigns/1234/LowerStack"
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_swimops_campaign(self, campaigns_api, auth_session, response):
        campaigns_api.get_swimops_campaign("1234")
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns/1234/Swimops")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()

    def test_get_swimops(self, campaigns_api, auth_session, response):
        campaigns_api.get_swimops()
        auth_session.get.assert_called_once_with("test_url/v1.0/Campaigns/Swimops")
        response.raise_for_status.assert_called_once()
        response.json.assert_called()
