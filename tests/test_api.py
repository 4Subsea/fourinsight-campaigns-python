import fourinsight.campaigns
from fourinsight.api.globalsettings import environment

import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def response():
    response = Mock()
    return response

@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session.get.return_value = response
    return auth_session


class Test_CampaignsAPI:

    def test_init(self):
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI("test")
        assert campaigns_api._auth_session == "test"

    def test_get_base_url(self):
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI("test")
        assert campaigns_api._get_base_url() == environment.api_base_url

    def test__get(self, auth_session, response):
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)
        assert campaigns_api._get("test") == response
        response.raise_for_status.assert_called_once()

    def test_verify_type(self, auth_session):
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)
        assert campaigns_api._verify_type("SWIM Campaign") == "SWIM Campaign"
        assert campaigns_api._verify_type("Campaign") == "Campaign"

    def test_verify_type_raises(self, auth_session):
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)
        with pytest.raises(ValueError):
            campaigns_api._verify_type("test")

    @patch("fourinsight.campaigns.api.environment")
    def test_get_campaigns(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_swim_campaigns(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api._get_swim_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/SWIM Campaign")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_generic_campaigns(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api._get_generic_campaigns()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/Campaign")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_campaigns_swim(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_campaigns(campaign_type="SWIM Campaign")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/SWIM Campaign")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_campaigns_generic(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_campaigns(campaign_type="Campaign")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Type/Campaign")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_campaigns_raises(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        with pytest.raises(ValueError):
            campaigns_api.get_campaigns(campaign_type="invalid_type")

    @patch("fourinsight.campaigns.api.environment")
    def test_get_campaign(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_campaign("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_events(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_events("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Events")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_sensors(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_sensors("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Sensors")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_lowerstack(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_lowerstack("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/LowerStack")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_swimops_campaign(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_swimops_campaign("1234")
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/1234/Swimops")
        response.json.assert_called()

    @patch("fourinsight.campaigns.api.environment")
    def test_get_swimops(self, env_mock, auth_session, response):
        env_mock.api_base_url = "test"
        campaigns_api = fourinsight.campaigns.api.CampaignsAPI(auth_session)

        campaigns_api.get_swimops()
        auth_session.get.assert_called_once_with(f"test/v1.0/Campaigns/Swimops")
        response.json.assert_called()
