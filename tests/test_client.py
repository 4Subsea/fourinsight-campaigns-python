import warnings
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
                "CampaignID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "string",
                "Type": "string",
                "Client": "string",
                "PO Number": "string",
                "Project Number": "string",
                "Vessel": "string",
                "Vessel Contractor": "string",
                "Well Name": "string",
                "Well ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Water Depth": 0.0,
                "Location": (1.3, 2.4),
                "Main Data Provider": "string",
                "Start Date": pd.to_datetime("2021-08-12T11:38:16.509Z"),
                "End Date": pd.to_datetime("2021-08-12T11:38:16.509Z"),
                "GeoTrack Position ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "GeoTrack Location": (3.2, 4.5),
                "GeoTrack Title": "string",
                "Hs Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Tp Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Wd Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
            {
                "CampaignID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "string",
                "Type": "string",
                "Client": "string",
                "PO Number": "string",
                "Project Number": "string",
                "Vessel": "string",
                "Vessel Contractor": "string",
                "Well Name": "string",
                "Well ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Water Depth": 0.0,
                "Location": (1.3, 2.4),
                "Main Data Provider": "string",
                "Start Date": pd.to_datetime("2021-08-12T11:38:16.509Z"),
                "End Date": pd.to_datetime("2021-08-12T11:38:16.509Z"),
                "GeoTrack Position ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "GeoTrack Location": (3.2, 4.5),
                "GeoTrack Title": "string",
                "Hs Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Tp Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Wd Timeseries ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        ]

        df_expected = pd.DataFrame.from_records(records, index="CampaignID")
        pd.testing.assert_frame_equal(df, df_expected)

    def test_get_campaign_type_generic(self, camp_client):
        assert camp_client._get_campaign_type("campaign") == GenericCampaign
        assert camp_client._get_campaign_type("Campaign") == GenericCampaign

    def test_get_campaign_type_swim(self, camp_client):
        assert camp_client._get_campaign_type("swim campaign") == SwimCampaign
        assert camp_client._get_campaign_type("Swim Campaign") == SwimCampaign

    @patch("fourinsight.campaigns.client.GenericCampaign")
    def test_get_generic(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_generic_id")
        mock_campaign.assert_called_once_with(auth_session, "test_generic_id")

    @patch("fourinsight.campaigns.client.SwimCampaign")
    def test_get_swim(self, mock_campaign, camp_client, auth_session):
        camp_client.get("test_swim_id")
        mock_campaign.assert_called_once_with(auth_session, "test_swim_id")
