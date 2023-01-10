import json
from unittest.mock import call

import pandas as pd
import pytest

import fourinsight.campaigns as fc
from fourinsight.campaigns.api import CampaignsAPI, JSONSpecialParse, _dict_rename


@pytest.fixture
def campaigns_api(auth_session):
    return CampaignsAPI(auth_session)


@pytest.fixture
def campaigns_api_camelcase(auth_session_camelcase):
    return CampaignsAPI(auth_session_camelcase)


@pytest.fixture
def headers_expect(auth_session):
    headers_expect = {
        "user-agent": auth_session.headers["user-agent"]
        + f" python-fourinsight-campaigns/{fc.__version__}"
    }
    return headers_expect


class Test_CampaignsAPI:
    def test_init(self, campaigns_api, auth_session):
        assert campaigns_api._session == auth_session

    def test__url_bare(self, campaigns_api):
        assert campaigns_api._url("") == "/v1.1/Campaigns"

    def test__url_something(self, campaigns_api):
        assert campaigns_api._url("something") == "/v1.1/Campaigns/something"
        assert campaigns_api._url("/something") == "/v1.1/Campaigns/something"

    def test__url_version(self, campaigns_api):
        assert (
            campaigns_api._url("", api_version="test_version")
            == "/test_version/Campaigns"
        )

    def test_get_geotrack(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_geotrack("1234")
        auth_session.get.assert_called_once_with(
            "/v1.0/Campaigns/1234",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = {
            "HS Timeseries Id": "e2ba4833-44ae-4cef-b8a7-18ae82fef327",
            "Tp Timeseries Id": "4cfe7e31-f4b5-471f-92c6-b260ee236cff",
            "Wd Timeseries Id": "2c6454b8-a274-4845-80e0-cb29c0efc32b",
        }
        assert expect == out

    def test_get_geotrack_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_geotrack("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.0/Campaigns/1234",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = {
            "HS Timeseries Id": "e2ba4833-44ae-4cef-b8a7-18ae82fef327",
            "Tp Timeseries Id": "4cfe7e31-f4b5-471f-92c6-b260ee236cff",
            "Wd Timeseries Id": "2c6454b8-a274-4845-80e0-cb29c0efc32b",
        }
        assert expect == out

    def test_get_campaigns(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_campaigns()
        call_list = [
            call(
                "/v1.1/Campaigns",
                headers=headers_expect,
            ),
            call(
                "campaigns next link",
                headers=headers_expect,
            ),
        ]
        auth_session.get.assert_has_calls(call_list)
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
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
        assert expect == out

    def test_get_campaigns_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_campaigns()
        call_list = [
            call(
                "/v1.1/Campaigns",
                headers=headers_expect,
            ),
            call(
                "campaigns next link",
                headers=headers_expect,
            ),
        ]
        auth_session_camelcase.get.assert_has_calls(call_list)
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
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
        assert expect == out

    def test_get_campaign(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_campaign("1234")
        auth_session.get.assert_called_once_with(
            "/v1.0/Campaigns/1234",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = {
            "CampaignID": "028ff3a8-2e08-463d-a4fe-bc10a53450ea",
            "Project Number": "0872",
            "Client": "Maersk Oil",
            "Vessel": "Ocean Valiant",
            "Vessel Contractor": "Diamond Offshore",
            "Well Name": "string",
            "Well ID": "2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Water Depth": 100.0,
            "Location": None,
            "Main Data Provider": "4Subsea",
            "Start Date": pd.to_datetime("2017-04-08T00:00:00+00:00"),
            "End Date": pd.to_datetime("2017-05-13T00:00:00+00:00"),
        }
        assert expect == out

    def test_get_campaign_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_campaign("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.0/Campaigns/1234",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = {
            "CampaignID": "028ff3a8-2e08-463d-a4fe-bc10a53450ea",
            "Project Number": "0872",
            "Client": "Maersk Oil",
            "Vessel": "Ocean Valiant",
            "Vessel Contractor": "Diamond Offshore",
            "Well Name": "string",
            "Well ID": "2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
            "Water Depth": 100.0,
            "Location": None,
            "Main Data Provider": "4Subsea",
            "Start Date": pd.to_datetime("2017-04-08T00:00:00+00:00"),
            "End Date": pd.to_datetime("2017-05-13T00:00:00+00:00"),
        }
        assert expect == out

    def test_get_events(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_events("1234")
        auth_session.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Events",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "Event Type": "string",
                "Comment": "string",
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            },
            {
                "Start": None,
                "End": None,
                "Event Type": "Artifact",
                "Comment": None,
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert expect == out

    def test_get_events_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_events("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Events",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "Event Type": "string",
                "Comment": "string",
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "WLR connected",
                "Comment": None,
            },
            {
                "Start": None,
                "End": None,
                "Event Type": "Artifact",
                "Comment": None,
            },
            {
                "Start": pd.to_datetime("2021-08-12T11:49:38.286Z"),
                "End": None,
                "Event Type": "Connect-Disconnect",
                "Comment": None,
            },
        ]
        assert expect == out

    def test_get_sensors(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_sensors("1234")
        call_list = [
            call(
                "/v1.1/Campaigns/1234/Sensors",
                headers=headers_expect,
            ),
            call(
                "/v1.1/Campaigns/1234/Sensors/3fa85f64-5717-4562-b3fc-2c963f66afa6/channels",
                headers=headers_expect,
            ),
        ]
        auth_session.get.assert_has_calls(call_list)
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
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
        assert expect == out

    def test_get_sensors_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_sensors("1234")
        call_list = [
            call(
                "/v1.1/Campaigns/1234/Sensors",
                headers=headers_expect,
            ),
            call(
                "/v1.1/Campaigns/1234/Sensors/3fa85f64-5717-4562-b3fc-2c963f66afa6/channels",
                headers=headers_expect,
            ),
        ]
        auth_session_camelcase.get.assert_has_calls(call_list)
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
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
        assert expect == out

    def test__get_sensors(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api._get_sensors("1234")
        auth_session.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Sensors",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
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
            },
        ]
        assert expect == out

    def test__get_sensors_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase._get_sensors("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Sensors",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
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
            },
        ]
        assert expect == out

    def test__get_channels(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api._get_channels("1234", "<wh sensor id>")
        auth_session.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Sensors/<wh sensor id>/channels",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
            {
                "Channel": "string",
                "Units": "string",
                "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        ]
        assert expect == out

    def test__get_channels_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase._get_channels("1234", "<wh sensor id>")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Sensors/<wh sensor id>/channels",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
            {
                "Channel": "string",
                "Units": "string",
                "Timeseries id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Stream id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        ]
        assert expect == out

    def test_get_lowerstack(
        self, campaigns_api, auth_session, response, headers_expect
    ):
        out = campaigns_api.get_lowerstack("1234")
        auth_session.get.assert_called_once_with(
            "/v1.0/Campaigns/1234/LowerStack",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = {
            "Alpha": 0.1,
            "Elements": [
                {
                    "Name": "string",
                    "Mass": 100.0,
                    "Submerged Weight": 1000.0,
                    "Height": 10.0,
                    "Added Mass Coefficient": 2.0,
                }
            ],
        }
        assert expect == out

    def test_get_lowerstack_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_lowerstack("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.0/Campaigns/1234/LowerStack",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = {
            "Alpha": 0.1,
            "Elements": [
                {
                    "Name": "string",
                    "Mass": 100.0,
                    "Submerged Weight": 1000.0,
                    "Height": 10.0,
                    "Added Mass Coefficient": 2.0,
                }
            ],
        }
        assert expect == out

    def test_get_swimops_campaign(
        self, campaigns_api, auth_session, response, headers_expect
    ):
        out = campaigns_api.get_swimops_campaign("1234")
        auth_session.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Swimops",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = {
            "Operation Status": "string",
            "Dashboard Status": "string",
            "SLA Level": "string",
            "Customer Contact": "string",
            "Comments": "string",
            "Dashboard Close Date": pd.to_datetime("2021-08-12T11:56:23.069Z"),
            "SWIM Instance Status": "string",
            "Report Made": "string",
            "Report Sent": "string",
            "Data Package Made": "string",
            "Data Package Sent": "string",
            "Experience Log Made": "string",
            "WellSpot Bending Moment Uploaded": "string",
            "Dashboard Closed": "string",
            "Services Available": "string",
        }
        expect == out

    def test_get_swimops_campaign_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_swimops_campaign("1234")
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.1/Campaigns/1234/Swimops",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = {
            "Operation Status": "string",
            "Dashboard Status": "string",
            "SLA Level": "string",
            "Customer Contact": "string",
            "Comments": "string",
            "Dashboard Close Date": pd.to_datetime("2021-08-12T11:56:23.069Z"),
            "SWIM Instance Status": "string",
            "Report Made": "string",
            "Report Sent": "string",
            "Data Package Made": "string",
            "Data Package Sent": "string",
            "Experience Log Made": "string",
            "WellSpot Bending Moment Uploaded": "string",
            "Dashboard Closed": "string",
            "Services Available": "string",
        }
        expect == out

    def test_get_swimops(self, campaigns_api, auth_session, response, headers_expect):
        out = campaigns_api.get_swimops()
        auth_session.get.assert_called_once_with(
            "/v1.1/Campaigns/Swimops",
            headers=headers_expect,
        )
        response.raise_for_status.assert_called()
        response.json.assert_called()
        expect = [
            {
                "Operation Status": "string",
                "Dashboard Status": "string",
                "SLA Level": "string",
                "Customer Contact": "string",
                "Comments": "string",
                "Dashboard Close Date": pd.to_datetime("2021-08-12T11:54:42.513Z"),
                "SWIM Instance Status": "string",
                "Report Made": "string",
                "Report Sent": "string",
                "Data Package Made": "string",
                "Data Package Sent": "string",
                "Experience Log Made": "string",
                "WellSpot Bending Moment Uploaded": "string",
                "Dashboard Closed": "string",
                "Services Available": "string",
            }
        ]
        assert expect == out

    def test_get_swimops_camelcase(
        self,
        campaigns_api_camelcase,
        auth_session_camelcase,
        response_camelcase,
        headers_expect,
    ):
        out = campaigns_api_camelcase.get_swimops()
        auth_session_camelcase.get.assert_called_once_with(
            "/v1.1/Campaigns/Swimops",
            headers=headers_expect,
        )
        response_camelcase.raise_for_status.assert_called()
        response_camelcase.json.assert_called()
        expect = [
            {
                "Operation Status": "string",
                "Dashboard Status": "string",
                "SLA Level": "string",
                "Customer Contact": "string",
                "Comments": "string",
                "Dashboard Close Date": pd.to_datetime("2021-08-12T11:54:42.513Z"),
                "SWIM Instance Status": "string",
                "Report Made": "string",
                "Report Sent": "string",
                "Data Package Made": "string",
                "Data Package Sent": "string",
                "Experience Log Made": "string",
                "WellSpot Bending Moment Uploaded": "string",
                "Dashboard Closed": "string",
                "Services Available": "string",
            }
        ]
        assert expect == out

    def test_get_campaign_type(self, campaigns_api, auth_session, response):
        assert campaigns_api.get_campaign_type("1234") == "swim campaign"

    def test_get_campaign_type_camelcase(
        self, campaigns_api_camelcase, auth_session_camelcase, response_camelcase
    ):
        assert campaigns_api_camelcase.get_campaign_type("1234") == "swim campaign"


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

    def test_location_invalid(self):
        json_str = """{
            "a_location": "1.23::4.56",
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": "7.89#10.11a#eight",
                    "nested_location_2": "twelve#14.15"
                }
            ]
        }"""

        dict_expected = {
            "a_location": "1.23::4.56",
            "b_other": "something",
            "nested": [
                {
                    "nested_location_1": (7.89, "10.11a#eight"),
                    "nested_location_2": ("twelve", 14.15),
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

    def test__float_valid(self):
        assert JSONSpecialParse._float(12.0) == 12.0
        assert JSONSpecialParse._float(12) == 12.0
        assert JSONSpecialParse._float("12") == 12.0

    def test__float_null(self):
        assert JSONSpecialParse._float("null") is None

    def test__float_invalid(self):
        assert JSONSpecialParse._float("12a") == "12a"
