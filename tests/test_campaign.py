import pandas as pd
from fourinsight.campaigns.api import CampaignsAPI
from fourinsight.campaigns.campaign import BaseCampaign

import pytest
from unittest.mock import patch


@pytest.fixture
def base_campaign(auth_session2):
    return BaseCampaign(auth_session2, "1234")


class Test_BaseCampaign:
    @patch.object(BaseCampaign, "_get_geotrack")
    @patch.object(BaseCampaign, "_get_events")
    @patch.object(BaseCampaign, "_get_sensors")
    @patch.object(BaseCampaign, "_get_campaign")
    def test_init(
        self,
        mock_get_campaign,
        mock_get_sensors,
        mock_get_events,
        mock_get_geotrack,
        auth_session2,
    ):
        base_campaign = BaseCampaign(auth_session2, "1234")

        assert base_campaign._campaign_id == "1234"
        assert isinstance(base_campaign._campaigns_api, CampaignsAPI)
        mock_get_campaign.assert_called_once_with("1234")
        assert base_campaign._campaign == mock_get_campaign.return_value
        mock_get_sensors.assert_called_once_with("1234")
        assert base_campaign._sensors == mock_get_sensors.return_value
        mock_get_events.assert_called_once_with("1234")
        assert base_campaign._events == mock_get_events.return_value
        mock_get_geotrack.assert_called_once_with("1234")
        assert base_campaign._geotrack == mock_get_geotrack.return_value

    def test_general(self, base_campaign):
        assert base_campaign.general() == base_campaign._campaign

    def test_geotrack(self, base_campaign):
        assert base_campaign.geotrack() == base_campaign._geotrack

    def test_events_value_none(self, base_campaign):
        events_out = base_campaign.events()
        events_expected = [
            {
                'Start': None,
                'End': None,
                'Event Type': 'Artifact',
                'Comment': None,
            },
            {
                'Start': pd.to_datetime("2019-01-01T00:00:00.0000000Z"),
                'End': None,
                'Event Type': 'WLR connected',
                'Comment': None,
            },
            {
                'Start': pd.to_datetime("2020-01-01T00:00:00.0000000Z"),
                'End': None,
                'Event Type': 'Connect-Disconnect',
                'Comment': None,
            },
        ]
        assert events_out == events_expected

    def test_events_value_connect_disconnect(self, base_campaign):
        events_out = base_campaign.events(value="Connect-Disconnect", by="Event Type")
        events_expected = [
            {
                'Start': pd.to_datetime('2020-01-01 00:00:00+0000'),
                'End': None,
                'Event Type': 'Connect-Disconnect',
                'Comment': None
            },
        ]
        assert events_out == events_expected

    def test_events_value_artifact(self, base_campaign):
        events_out = base_campaign.events(value="Artifact", by="Event Type")
        events_expected = [
            {
                'Start': None,
                'End': None,
                'Event Type': 'Artifact',
                'Comment': None
            },
        ]
        assert events_out == events_expected

    def test_events_value_wlr_connected(self, base_campaign):
        events_out = base_campaign.events(value="WLR connected", by="Event Type")
        events_expected = [
            {
                'Start': pd.to_datetime("2019-01-01T00:00:00.0000000Z"),
                'End': None,
                'Event Type': 'WLR connected',
                'Comment': None
                }
        ]
        assert events_out == events_expected

    def test_events_raises(self, base_campaign):
        with pytest.raises(RuntimeError):
            base_campaign.events(value="invalid_value", by="Event Type")

    def test_sort_list_by_start(self):
        list_ = [
            {"Start": "2020-01-01T00:00:00+0000"},
            {"Start": None},
            {"Start": pd.to_datetime("2019-01-01T00:00:00+0000")},
        ]

        list_out = BaseCampaign._sort_list_by_start(list_)
        list_expect = [
            {"Start": None},
            {"Start": pd.to_datetime("2019-01-01T00:00:00+0000")},
            {"Start": "2020-01-01T00:00:00+0000"},
        ]
        assert list_out == list_expect
