from fourinsight.campaigns import Client
from fourinsight.campaigns.campaign import GenericCampaign, SwimCampaign

import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def auth_session():
    auth_session = Mock()
    return auth_session


@pytest.fixture
def camp_client(auth_session):
    return Client(auth_session)


class Test_Client:
    def test_init(self, camp_client, auth_session):
        assert camp_client._auth_session == auth_session

    def test_get_campaign_type_generic(self, camp_client):
        camp_client._get_campaign_type("generic") == GenericCampaign
        camp_client._get_campaign_type("Generic") == GenericCampaign

    def test_get_campaign_type_swim(self, camp_client):
        camp_client._get_campaign_type("swim") == SwimCampaign
        camp_client._get_campaign_type("Swim") == SwimCampaign

    def test_get_campaign_type_raises(self, camp_client):
        with pytest.raises(ValueError):
            camp_client._get_campaign_type("invalid_type")

    @patch("fourinsight.campaigns.client.GenericCampaign")
    def test_get_default(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_id")
        mock_campaign.assert_called_once_with(auth_session, "test_id")

    @patch("fourinsight.campaigns.client.GenericCampaign")
    def test_get_generic(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_id", campaign_type="generic")
        mock_campaign.assert_called_once_with(auth_session, "test_id")

    @patch("fourinsight.campaigns.client.SwimCampaign")
    def test_get_generic(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_id", campaign_type="swim")
        mock_campaign.assert_called_once_with(auth_session, "test_id")
