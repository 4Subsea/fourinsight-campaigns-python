import pandas as pd
from fourinsight.campaigns.api import CampaignsAPI
from fourinsight.campaigns.campaign import BaseCampaign, GenericCampaign, SwimCampaign

import pytest
from unittest.mock import patch


@pytest.fixture
def base_campaign(auth_session2):
    return BaseCampaign(auth_session2, "1234")

@pytest.fixture
def swim_campaign(auth_session2):
    return SwimCampaign(auth_session2, "1234")


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
            {"Start": None, "End": None, "Event Type": "Artifact", "Comment": None,},
            {
                "Start": pd.to_datetime("2019-01-01T00:00:00.0000000Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            },
            {
                "Start": pd.to_datetime("2020-01-01T00:00:00.0000000Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert events_out == events_expected

    def test_events_value_connect_disconnect(self, base_campaign):
        events_out = base_campaign.events(value="Connect-Disconnect", by="Event Type")
        events_expected = [
            {
                "Start": pd.to_datetime("2020-01-01 00:00:00+0000"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert events_out == events_expected

    def test_events_value_artifact(self, base_campaign):
        events_out = base_campaign.events(value="Artifact", by="Event Type")
        events_expected = [
            {"Start": None, "End": None, "Event Type": "Artifact", "Comment": None},
        ]
        assert events_out == events_expected

    def test_events_value_wlr_connected(self, base_campaign):
        events_out = base_campaign.events(value="WLR connected", by="Event Type")
        events_expected = [
            {
                "Start": pd.to_datetime("2019-01-01T00:00:00.0000000Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            }
        ]
        assert events_out == events_expected

    def test_events_raises(self, base_campaign):
        with pytest.raises(RuntimeError):
            base_campaign.events(value="NOEXIST", by="Event Type")

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

    def test_sensor_value_none(self, base_campaign):
        sensors_out = base_campaign.sensors(value=None)
        sensors_expect = [
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN1234",
                "Position": "LMRP",
                "Distance From Wellhead": "string",
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": "string",
                "Sensor Vendor": "string",
                "Attached Time": pd.to_datetime("2019-10-13 09:27:19+0000"),
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "Pitch",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN5678",
                "Position": "WH",
                "Distance From Wellhead": "string",
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": "string",
                "Sensor Vendor": "string",
                "Attached Time": None,
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "Ag",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_by_position(self, base_campaign):
        sensors_out = base_campaign.sensors(value="LMRP", by="Position")
        sensors_expect = [
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN1234",
                "Position": "LMRP",
                "Distance From Wellhead": "string",
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": "string",
                "Sensor Vendor": "string",
                "Attached Time": pd.to_datetime("2019-10-13 09:27:19+0000"),
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "Pitch",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_by_name(self, base_campaign):
        sensors_out = base_campaign.sensors(value="SN5678", by="Name")
        sensors_expect = [
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN5678",
                "Position": "WH",
                "Distance From Wellhead": "string",
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": "string",
                "Sensor Vendor": "string",
                "Attached Time": None,
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "Ag",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ],
            },
        ]
        assert sensors_out == sensors_expect

    def test_sensor_raises(self, base_campaign):
        with pytest.raises(RuntimeError):
            base_campaign.sensors(value="NOEXIST")

    def test_filter_dict_value_by(self, base_campaign):
        dict_list = [
            {"A": "some-value", "B": None},
            {"A": "string", "B": 1},
            {"A": None, "B": None},
        ]

        out = BaseCampaign._filter_dict_value_by(dict_list, "some-value", "A")
        expect = [{"A": "some-value", "B": None}]
        assert out == expect

        out = BaseCampaign._filter_dict_value_by(dict_list, None, "B")
        expect = [{"A": "some-value", "B": None}, {"A": None, "B": None}]
        assert out == expect

    def test_dict_subset(self):
        dict_ = {"A0": 1, "B0": "string", "C0": None}
        out = BaseCampaign._dict_subset(dict_, {"A0": "a1", "B0": "b1"})
        expect = {"a1": 1, "b1": "string"}
        assert out == expect

    def test_get_campaign(self, base_campaign):
        out = base_campaign._get_campaign("1234")
        expect = {
            "CampaignID": "028ff3a8-2e08-463d-a4fe-bc10a53450ea",
            "Project Number": "0872",
            "Client": "Maersk Oil",
            "Vessel": "Ocean Valiant",
            "Vessel Contractor": "Diamond Offshore",
            "Well Name": "Could not fetch well 2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Well ID": "2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Water Depth": None,
            "Location": None,
            "Main Data Provider": "4Subsea",
            "Start Date": pd.to_datetime("2017-04-08 00:00:00+0000"),
            "End Date": pd.to_datetime("2017-05-13 00:00:00+0000"),
        }
        assert out == expect

    def test_get_geotrack(self, base_campaign):
        out = base_campaign._get_geotrack("1234")
        expect = {
            'HS Timeseries Id': 'e2ba4833-44ae-4cef-b8a7-18ae82fef327',
            'Tp Timeseries Id': '4cfe7e31-f4b5-471f-92c6-b260ee236cff',
            'Wd Timeseries Id': '2c6454b8-a274-4845-80e0-cb29c0efc32b'
        }
        assert out == expect

    def test_get_events(self, base_campaign):
        out = base_campaign._get_events("1234")
        expect = [
            {
                'Start': pd.to_datetime('2020-01-01 00:00:00+0000'),
                'End': None,
                'Event Type': 'Connect-Disconnect',
                'Comment': None
            },
            {
                'Start': None,
                'End': None,
                'Event Type': 'Artifact',
                'Comment': None
            },
            {
                'Start': pd.to_datetime('2019-01-01 00:00:00+0000'),
                'End': None,
                'Event Type': 'WLR connected',
                'Comment': None
            }
        ]
        assert out == expect

    def test_get_sensors(self, base_campaign):
        out = base_campaign._get_sensors("1234")
        expect = [
            {
                'SensorID': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'Name': 'SN1234',
                'Position': 'LMRP',
                'Distance From Wellhead': 'string',
                'Direction X Axis': 'string',
                'Direction Z Axis': 'string',
                'Sampling Rate': 'string',
                'Sensor Vendor': 'string',
                'Attached Time': pd.to_datetime('2019-10-13 09:27:19+0000'),
                'Detached Time': None,
                'Channels': [
                    {
                        'Channel': 'Pitch',
                        'Units': 'string',
                        'Timeseries id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                        'Stream id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'
                    }
                ]
            },
            {
                'SensorID': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'Name': 'SN5678',
                'Position': 'WH',
                'Distance From Wellhead': 'string',
                'Direction X Axis': 'string',
                'Direction Z Axis': 'string',
                'Sampling Rate': 'string',
                'Sensor Vendor': 'string',
                'Attached Time': None,
                'Detached Time': None,
                'Channels': [
                    {
                        'Channel': 'Ag',
                        'Units': 'string',
                        'Timeseries id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                        'Stream id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'
                    }
                ]
            }
        ]
        assert out == expect


def test_generic_campaign_is_base_campaign(auth_session2):
    generic_campaign = GenericCampaign(auth_session2, "1234")
    assert isinstance(generic_campaign, BaseCampaign)


class Test_SwimCampaign:
    def test_inherit(self, swim_campaign):
        assert isinstance(swim_campaign, BaseCampaign)

    @patch.object(BaseCampaign, "__init__")
    @patch.object(SwimCampaign, "_get_swim_operations")
    def test_init(self, mock_get_swimops, mock_base_init, auth_session2):
        swim_campaign = SwimCampaign(auth_session2, "1234")
        assert swim_campaign._swim_operations == mock_get_swimops.return_value
        mock_base_init.assert_called_once_with(auth_session2, "1234")

    def test_get_swim_operations(self, swim_campaign):
        out = swim_campaign._get_swim_operations("1234")
        expect = {
            'Operation Status': 'string',
            'Dashboard Status': 'string',
            'SLA Level': 'string',
            'Customer Contact': 'string',
            'Comments': 'string',
            'Dashboard Close Date': 'string',
            'SWIM Instance Status': 'string',
            'Report Made': 'string',
            'Report Sent': 'string',
            'Data Package Made': 'string',
            'Data Package Sent': 'string',
            'Experience Log Made': 'string',
            'WellSpot Bending Moment Uploaded':'string',
            'Dashboard Closed': 'string',
            'Services Available': 'string'
        }
        assert out == expect

    def test_swim_operations(self, swim_campaign):
        assert swim_campaign.swim_operations() == swim_campaign._swim_operations
