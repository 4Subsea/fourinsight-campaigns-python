from unittest.mock import call, patch

import pandas as pd
import pytest

from fourinsight.campaigns import channels as Channels
from fourinsight.campaigns.campaign import GenericCampaign, SwimCampaign


@pytest.fixture
def generic_campaign(auth_session):
    return GenericCampaign(auth_session, "1234")


@pytest.fixture
def swim_campaign(auth_session):
    return SwimCampaign(auth_session, "1234")


# def assert_list_of_dicts_equal(list1, list2):
#     assert [e for e in list1 if e not in list2] == []


class Test_GenericCampaign:
    def test_init(
        self,
        auth_session,
    ):
        generic_campaign = GenericCampaign(auth_session, "1234")

        assert generic_campaign._campaign_id == "1234"
        for attr in ["_campaign", "_events", "_sensors", "_geotrack"]:
            assert hasattr(generic_campaign, attr)

    def test_general(self, generic_campaign):
        assert generic_campaign.general() == generic_campaign._campaign

    def test_lazy_load(self, generic_campaign):
        with patch.object(generic_campaign._campaigns_api, "get_campaign") as mock_get:
            mock_get.return_value = {"abc": 123}

            out_1 = generic_campaign.general()
            out_2 = generic_campaign.general()
        assert {"abc": 123} == out_1
        assert out_1 == out_2
        mock_get.assert_called_once_with("1234")

    def test_geotrack(self, generic_campaign):
        assert generic_campaign.geotrack() == generic_campaign._geotrack

    def test_events_value_none(self, generic_campaign):
        events_out = generic_campaign.events()
        events_expected = [
            {
                "Start": None,
                "End": None,
                "Event Type": "Artifact",
                "Comment": None
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "Event Type": "string",
                "Comment": "string"
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert events_out == events_expected
        # import unittest
        # unittest.TestCase().assertCountEqual(events_out, events_expected)
        # assert [e for e in events_out if e not in events_expected] == []
        # assert_list_of_dicts_equal(events_out, events_expected)

    def test_events_value_connect_disconnect(self, generic_campaign):
        events_out = generic_campaign.events(
            value="Connect-Disconnect", by="Event Type"
        )
        events_expected = [
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert events_out == events_expected

    def test_events_value_artifact(self, generic_campaign):
        events_out = generic_campaign.events(value="Artifact", by="Event Type")
        events_expected = [
            {"Start": None, "End": None, "Event Type": "Artifact", "Comment": None},
        ]
        assert events_out == events_expected

    def test_events_value_wlr_connected(self, generic_campaign):
        events_out = generic_campaign.events(value="WLR connected", by="Event Type")
        events_expected = [
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            }
        ]
        assert events_out == events_expected

    def test_events_raises(self, generic_campaign):
        with pytest.raises(RuntimeError):
            generic_campaign.events(value="NOEXIST", by="Event Type")

    def test_sort_list_by_start(self):
        list_ = [
            {"Start": "2020-01-01T00:00:00+0000"},
            {"Start": None},
            {"Start": pd.to_datetime("2019-01-01T00:00:00+0000")},
        ]

        list_out = GenericCampaign._sort_list_by_start(list_)
        list_expect = [
            {"Start": None},
            {"Start": pd.to_datetime("2019-01-01T00:00:00+0000")},
            {"Start": "2020-01-01T00:00:00+0000"},
        ]
        assert list_out == list_expect

    def test_sensor_value_none(self, generic_campaign):
        sensors_out = generic_campaign.sensors(value=None)
        sensors_expect = [
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "string",
                "Position": "string",
                "Distance From Wellhead": 0.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 0.0,
                "Sensor Vendor": "string",
                "Attached Time": pd.to_datetime("2021-08-12T11:51:19.667Z"),
                "Detached Time": pd.to_datetime("2021-08-12T11:51:19.667Z"),
                "Channels": [
                    {
                        "Channel": "string",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
            {
                "SensorID": "<wh sensor id>",
                "Name": "SN1234",
                "Position": "WH",
                "Distance From Wellhead": 0.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 0.0,
                "Sensor Vendor": "string",
                "Attached Time": None,
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "string",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_by_position(self, generic_campaign):
        sensors_out = generic_campaign.sensors(value="WH", by="Position")
        sensors_expect = [
            {
                "SensorID": "<wh sensor id>",
                "Name": "SN1234",
                "Position": "WH",
                "Distance From Wellhead": 0.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 0.0,
                "Sensor Vendor": "string",
                "Attached Time": None,
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "string",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_by_name(self, generic_campaign):
        sensors_out = generic_campaign.sensors(value="SN1234", by="Name")
        sensors_expect = [
            {
                "SensorID": "<wh sensor id>",
                "Name": "SN1234",
                "Position": "WH",
                "Distance From Wellhead": 0.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 0.0,
                "Sensor Vendor": "string",
                "Attached Time": None,
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "string",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_raises(self, generic_campaign):
        with pytest.raises(RuntimeError):
            generic_campaign.sensors(value="NOEXIST")

    def test_filter_dict_value_by(self, generic_campaign):
        dict_list = [
            {"A": "some-value", "B": None},
            {"A": "string", "B": 1},
            {"A": None, "B": None},
        ]

        out = GenericCampaign._filter_dict_value_by(dict_list, "some-value", "A")
        expect = [{"A": "some-value", "B": None}]
        assert out == expect

        out = GenericCampaign._filter_dict_value_by(dict_list, None, "B")
        expect = [{"A": "some-value", "B": None}, {"A": None, "B": None}]
        assert out == expect

    def test_dict_subset(self):
        dict_ = {"A0": 1, "B0": "string", "C0": None}
        out = GenericCampaign._dict_subset(dict_, {"A0": "a1", "B0": "b1"})
        expect = {"a1": 1, "b1": "string"}
        assert out == expect

    @patch("fourinsight.campaigns.campaign.download_sensor_data", return_value="abc")
    def test_get_sensor_data(self, mock_dl_data, generic_campaign):
        campaign = generic_campaign
        start = pd.to_datetime("2019-01-01")
        end = pd.to_datetime("2019-02-01")
        campaign._campaign = {"Start Date": start, "End Date": end}
        channels = [
            {"Channel": "c1", "Timeseries id": "ts1"},
            {"Channel": "c2", "Timeseries id": "ts2"},
        ]
        result = campaign.get_sensor_data("dummy_client", {"Channels": channels})

        mock_dl_data.assert_called_once_with(
            "dummy_client",
            {"c1": "ts1", "c2": "ts2"},
            start=start,
            end=end + pd.to_timedelta("1D"),
        )
        assert result == "abc"

    @patch("fourinsight.campaigns.campaign.download_sensor_data")
    def test_get_sensor_data_whitelist(self, mock_dl_data, generic_campaign):
        campaign = generic_campaign
        start = pd.to_datetime("2019-01-01")
        end = pd.to_datetime("2019-02-01")
        campaign._campaign = {"Start Date": start, "End Date": end}
        channels = [
            {"Channel": "c1", "Timeseries id": "ts1"},
            {"Channel": "c2", "Timeseries id": "ts2"},
        ]
        campaign.get_sensor_data("dummy_client", {"Channels": channels}, filter_=["c2"])

        mock_dl_data.assert_called_once_with(
            "dummy_client", {"c2": "ts2"}, start=start, end=end + pd.to_timedelta("1D")
        )

    @patch("fourinsight.campaigns.campaign.download_sensor_data")
    def test_get_sensor_data_whitelist_with_channels(
        self, mock_dl_data, generic_campaign
    ):
        campaign = generic_campaign
        start = pd.to_datetime("2019-01-01")
        end = pd.to_datetime("2019-02-01")
        campaign._campaign = {"Start Date": start, "End Date": end}
        channels = [
            {"Channel": "Ax", "Timeseries id": "ts1"},
            {"Channel": "Gx", "Timeseries id": "ts2"},
        ]
        campaign.get_sensor_data(
            "dummy_client", {"Channels": channels}, filter_=Channels.G
        )

        mock_dl_data.assert_called_once_with(
            "dummy_client", {"Gx": "ts2"}, start=start, end=end + pd.to_timedelta("1D")
        )

    @patch("fourinsight.campaigns.campaign.pd.isna", return_value=True)
    @patch("fourinsight.campaigns.campaign.download_sensor_data")
    def test_get_sensor_data_start_end_is_na(
        self, mock_dl_data, mock_isna, generic_campaign
    ):
        campaign = generic_campaign
        start = pd.to_datetime("NaT")
        end = pd.to_datetime("NaT")
        campaign._campaign = {"Start Date": start, "End Date": end}
        channels = [
            {"Channel": "c1", "Timeseries id": "ts1"},
            {"Channel": "c2", "Timeseries id": "ts2"},
        ]
        campaign.get_sensor_data("dummy_client", {"Channels": channels})

        mock_dl_data.assert_called_once_with(
            "dummy_client", {"c1": "ts1", "c2": "ts2"}, end="now", start=None
        )

    @patch("fourinsight.campaigns.campaign.download_sensor_data")
    def test_get_sensor_data_start_end_is_set(self, mock_dl_data, generic_campaign):
        campaign = generic_campaign
        start = pd.to_datetime("2019-01-01")
        end = pd.to_datetime("2019-02-01")
        start_custom = pd.to_datetime("2019-07-01")
        end_custom = pd.to_datetime("2019-07-05")
        campaign._campaign = {"Start Date": start, "End Date": end}
        channels = [
            {"Channel": "c1", "Timeseries id": "ts1"},
            {"Channel": "c2", "Timeseries id": "ts2"},
        ]
        campaign.get_sensor_data(
            "dummy_client", {"Channels": channels}, start=start_custom, end=end_custom
        )

        mock_dl_data.assert_called_once_with(
            "dummy_client",
            {"c1": "ts1", "c2": "ts2"},
            start=start_custom,
            end=end_custom,
        )


class Test_SwimCampaign:
    def test_inherit(self, swim_campaign):
        assert isinstance(swim_campaign, GenericCampaign)

    def test_init(self, auth_session):
        swim_campaign = SwimCampaign(auth_session, "1234")

        assert swim_campaign._campaign_id == "1234"
        for attr in [
            "_campaign",
            "_events",
            "_sensors",
            "_geotrack",
            "_lowerstack",
            "_swim_operations",
        ]:
            assert hasattr(swim_campaign, attr)

    def test_swim_operations(self, swim_campaign):
        assert swim_campaign.swim_operations() == swim_campaign._swim_operations

    def test_lowerstack(self, swim_campaign):
        assert swim_campaign.lowerstack() == swim_campaign._lowerstack
