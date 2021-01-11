import json

import pandas as pd
import pytest

from fourinsight.campaigns.api import CampaignsAPI, JSONSpecialParse, _dict_rename


@pytest.fixture
def campaigns_api(auth_session):
    return CampaignsAPI(auth_session)


class Test_CampaignsAPI:
    def test_init(self, campaigns_api, auth_session):
        assert campaigns_api._session == auth_session
        assert campaigns_api._api_version == "v1.0"

    def test__url_bare(self, campaigns_api):
        assert campaigns_api._url("") == "/v1.0/Campaigns"

    def test__url_something(self, campaigns_api):
        assert campaigns_api._url("something") == "/v1.0/Campaigns/something"
        assert campaigns_api._url("/something") == "/v1.0/Campaigns/something"

    def test_get_campaigns(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_campaigns()
        auth_session.get.assert_called_once_with("/v1.0/Campaigns")
        response.json.assert_called()
        expect = [
            {
                "CampaignID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "1086 - 31/2-F-6",
                "Type": "SWIM Campaign",
                "Client": "string",
                "PO Number": "string",
                "Project Number": "string",
                "Vessel": "Songa Endurance",
                "Vessel Contractor": "string",
                "Well Name": "31/2-F-6",
                "Well ID": "string",
                "Water Depth": 100.0,
                "Location": (1.3, 2.4),
                "Main Data Provider": "string",
                "Start Date": pd.to_datetime("2021-01-05T13:49:51.815Z"),
                "End Date": pd.to_datetime("2021-01-05T13:49:51.815Z"),
                "GeoTrack Position ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "GeoTrack Location": (3.2, 4.5),
                "GeoTrack Title": "string",
                "Hs Timeseries ID": "string",
                "Tp Timeseries ID": "string",
                "Wd Timeseries ID": "string",
            }
        ]
        assert expect == out

    def test_get_campaign(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_campaign("1234")
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/1234")
        response.json.assert_called()
        expect = {
            "CampaignID": "028ff3a8-2e08-463d-a4fe-bc10a53450ea",
            "Project Number": "0872",
            "Client": "Maersk Oil",
            "Vessel": "Ocean Valiant",
            "Vessel Contractor": "Diamond Offshore",
            "Well Name": "Could not fetch well 2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Well ID": "2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Water Depth": 100.0,
            "Location": None,
            "Main Data Provider": "4Subsea",
            "Start Date": pd.to_datetime("2017-04-08T00:00:00+00:00"),
            "End Date": pd.to_datetime("2017-05-13T00:00:00+00:00"),
        }
        assert expect == out

    def test_get_events(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_events("1234")
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/1234/Events")
        response.json.assert_called()
        expect = [
            {
                "Start": pd.to_datetime("2020-01-01T00:00:00.0000000Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
            {
                "Start": None,
                "End": None,
                "Event Type": "Artifact",
                "Comment": None,
            },
            {
                "Start": pd.to_datetime("2019-01-01T00:00:00.0000000Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            }
        ]
        assert expect == out

    def test_get_sensors(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_sensors("1234")
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/1234/Sensors")
        response.json.assert_called()
        expect = [
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN1234",
                "Position": "LMRP",
                "Distance From Wellhead": 3.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 10.24,
                "Sensor Vendor": "string",
                "Attached Time": pd.to_datetime("2019-10-13T09:27:19.0000000Z"),
                "Detached Time": None,
                "Channels": [
                    {
                        "Channel": "Pitch",
                        "Units": "string",
                        "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }
                ]
            },
            {
                "SensorID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Name": "SN5678",
                "Position": "WH",
                "Distance From Wellhead": 3.0,
                "Direction X Axis": "string",
                "Direction Z Axis": "string",
                "Sampling Rate": 10.24,
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
                ]
            }
        ]
        assert expect == out

    def test_get_lowerstack(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_lowerstack("1234")
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/1234/LowerStack")
        response.json.assert_called()
        expect = {
            "Alpha": 0.1,
            "Elements": [
                {
                    "Name": "string",
                    "Mass": 100.0,
                    "Submerged Weight": 1000.0,
                    "Height": 10.0,
                    "Added Mass Coefficient": 2.0
                }
            ]
        }
        assert expect == out

    def test_get_swimops_campaign(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_swimops_campaign("1234")
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/1234/Swimops")
        response.json.assert_called()
        expect = {
            "Operation Status": "string",
            "Dashboard Status": "string",
            "SLA Level": "string",
            "Customer Contact": "string",
            "Comments": "string",
            "Dashboard Close Date": pd.to_datetime("2020-10-21T13:12:09.814Z"),
            "SWIM Instance Status": "string",
            "Report Made": "string",
            "Report Sent": "string",
            "Data Package Made": "string",
            "Data Package Sent": "string",
            "Experience Log Made": "string",
            "WellSpot Bending Moment Uploaded": "string",
            "Dashboard Closed": "string",
            "Services Available": "string"
        }
        expect == out

    def test_get_swimops(self, campaigns_api, auth_session, response):
        out = campaigns_api.get_swimops()
        auth_session.get.assert_called_once_with("/v1.0/Campaigns/Swimops")
        response.json.assert_called()
        expect = [
            {
                "Operation Status": "string",
                "Dashboard Status": "string",
                "SLA Level": "string",
                "Customer Contact": "string",
                "Comments": "string",
                "Dashboard Close Date": pd.to_datetime("2020-10-21T13:12:09.814Z"),
                "SWIM Instance Status": "string",
                "Report Made": "string",
                "Report Sent": "string",
                "Data Package Made": "string",
                "Data Package Sent": "string",
                "Experience Log Made": "string",
                "WellSpot Bending Moment Uploaded": "string",
                "Dashboard Closed": "string",
                "Services Available": "string"
            }
        ]
        assert expect == out

    def test_get_campaign_type(self, campaigns_api, auth_session, response):
        assert campaigns_api.get_campaign_type("1234") == "swim campaign"


class Test__dict_rename:
    def test_rename(self):
        dict_org = {
            "a": "this",
            "b": {"one": 1, "two": 2},
            "c": "ignore me",
            "d": [
                {"tell": "me", "why": "!"},
                {"tell": "you", "why": "?"},
            ],
        }

        dict_map = {
            ("a", "A"): None,
            ("b", "b"): {("one", "One"): None, ("two", "TWO"): None},
            ("d", "D"): {("tell", "Tell"): None, ("why", "WHY"): None},
        }

        dict_expected = {
            "A": "this",
            "b": {"One": 1, "TWO": 2},
            "D": [
                {"Tell": "me", "WHY": "!"},
                {"Tell": "you", "WHY": "?"},
            ],
        }

        dict_out = _dict_rename(dict_org, dict_map)
        assert dict_expected == dict_out


class Test_JSONSpecialParse:
    def test_datetime(self):
        json_str = """{
            "a_datetime": "2020-01-01 00:01:00Z",
            "b_other": "something",
            "nested": [
                {
                    "nested_datetime_1": "2020-01-01 00:02:00Z",
                    "nested_datetime_2": "2020-01-01 00:03:00Z"
                }
            ]
        }"""

        dict_expected = {
            "a_datetime": pd.to_datetime("2020-01-01 00:01:00Z"),
            "b_other": "something",
            "nested": [
                {
                    "nested_datetime_1": pd.to_datetime("2020-01-01 00:02:00Z"),
                    "nested_datetime_2": pd.to_datetime("2020-01-01 00:03:00Z"),
                }
            ],
        }

        json_special_hook = JSONSpecialParse(
            datetime_keys=("a_datetime", "nested_datetime_1", "nested_datetime_2")
        )

        dict_out = json.loads(json_str, object_hook=json_special_hook)
        assert dict_expected == dict_out

    def test_location(self):
        json_str = """{
            "a_location": "1.23#4.56",
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": "7.89#10.11",
                    "nested_location_2": "12.13#14.15"
                }
            ]
        }"""

        dict_expected = {
            "a_location": (1.23, 4.56),
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": (7.89, 10.11),
                    "nested_location_2": (12.13, 14.15),
                }
            ],
        }

        json_special_hook = JSONSpecialParse(
            location_keys=("a_location", "nested_location_1", "nested_location_2")
        )

        dict_out = json.loads(json_str, object_hook=json_special_hook)
        assert dict_expected == dict_out

    def test_location_null(self):
        json_str = """{
            "a_location": "null#null",
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": "null#10.11",
                    "nested_location_2": "12.13#null"
                }
            ]
        }"""

        dict_expected = {
            "a_location": (None, None),
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": (None, 10.11),
                    "nested_location_2": (12.13, None),
                }
            ],
        }

        json_special_hook = JSONSpecialParse(
            location_keys=("a_location", "nested_location_1", "nested_location_2")
        )

        dict_out = json.loads(json_str, object_hook=json_special_hook)
        assert dict_expected == dict_out

    def test_numbers(self):
        """Deprecate when REST API endpoint starts returning native values"""
        json_str = """{
            "a_float": "1.23",
            "b_other": "something",
            "nested": [
                {
                    "nested_float_1": "7.89",
                    "nested_int_2": "12"
                }
            ]
        }"""

        dict_expected = {
            "a_float": 1.23,
            "b_other": "something",
            "nested": [{"nested_float_1": 7.89, "nested_int_2": 12}],
        }

        json_special_hook = JSONSpecialParse(
            float_keys=("a_float", "nested_float_1"), int_keys=("nested_int_2",)
        )

        dict_out = json.loads(json_str, object_hook=json_special_hook)
        assert dict_expected == dict_out

    def test_mixed(self):
        json_str = """{
            "a_location": "1.23#4.56",
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": "7.89#10.11",
                    "nested_datetime_2": "2020-01-01 04:00:12Z"
                }
            ]
        }"""

        dict_expected = {
            "a_location": (1.23, 4.56),
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": (7.89, 10.11),
                    "nested_datetime_2": pd.to_datetime("2020-01-01 04:00:12Z"),
                }
            ],
        }

        json_special_hook = JSONSpecialParse(
            location_keys=("a_location", "nested_location_1"),
            datetime_keys=("nested_datetime_2",),
        )

        dict_out = json.loads(json_str, object_hook=json_special_hook)
        assert dict_expected == dict_out
