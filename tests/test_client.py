from unittest.mock import patch

import pandas as pd
import pytest
from fourinsight.campaigns import Client
from fourinsight.campaigns.campaign import GenericCampaign, SwimCampaign


@pytest.fixture
def camp_client(auth_session):
    return Client(auth_session)


class Test_Client:
    def test_init(self, camp_client, auth_session):
        assert camp_client._session == auth_session

    def test_overview(self, camp_client, auth_session):
        df = camp_client.overview()

        records = [
            {
                "CampaignID": "6c181d43-0fba-425c-b8bf-06dfb4a661db",
                "Name": "1086 - 31/2-F-6",
                "Type": "SWIM Campaign",
                "Vessel": "Songa Endurance",
                "Field": "Troll",
                "Well Name": "31/2-F-6",
                "Start Date": pd.to_datetime("2017-10-21T00:00:00+00:00"),
            }
        ]
        df_expected = pd.DataFrame.from_records(records, index="CampaignID")
        pd.testing.assert_frame_equal(df, df_expected)

    def test_get_campaign_type_generic(self, camp_client):
        camp_client._get_campaign_type("generic") == GenericCampaign
        camp_client._get_campaign_type("Generic") == GenericCampaign

    def test_get_campaign_type_swim(self, camp_client):
        camp_client._get_campaign_type("swim") == SwimCampaign
        camp_client._get_campaign_type("Swim") == SwimCampaign

    # def test_get_campaign_type_raises(self, camp_client):
    #     with pytest.raises(ValueError):
    #         camp_client._get_campaign_type("invalid_type")

    # @patch("fourinsight.campaigns.client.GenericCampaign")
    # def test_get_default(self, mock_campaign, camp_client, auth_session):
    #     camp_client.get("test_id")
    #     mock_campaign.assert_called_once_with(auth_session, "test_id")

    # @patch("fourinsight.campaigns.client.GenericCampaign")
    # def test_get_generic(self, mock_campaign, camp_client, auth_session):
    #     camp_client.get("test_id", campaign_type="generic")
    #     mock_campaign.assert_called_once_with(auth_session, "test_id")

    # @patch("fourinsight.campaigns.client.SwimCampaign")
    # def test_get_swim(self, mock_campaign, camp_client, auth_session):
    #     camp_client.get("test_id", campaign_type="swim")
    #     mock_campaign.assert_called_once_with(auth_session, "test_id")

    @patch("fourinsight.campaigns.client.GenericCampaign")
    def test_get_generic(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_generic_id")
        mock_campaign.assert_called_once_with(auth_session, "test_generic_id")

    @patch("fourinsight.campaigns.client.SwimCampaign")
    def test_get_swim(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_swim_id")
        mock_campaign.assert_called_once_with(auth_session, "test_swim_id")
