import pandas as pd

import fourinsight.campaigns as fc


def _dict_rename(dict_org, dict_map):
    """
    Recursively rename and filter dict keys.

    Parameters
    ----------
    dict_org : dict
        Original dictionary.
    dict_map : dict
        Dictionary mapping old-to-new key names. See Notes.

    Returns
    -------
    dict_new: dict
        Key-renamed and filetered copy of 'dict_org'.

    Notes
    -----
    'dict_map' is used to rename and filter keys. Eg.

    'dict_org = {"a": 1, "b": {"one": 1, "two": 2}, "c": 3}' and
    'dict_map = {("a", "A"): None, ("b", "B"): {("one", "One"): None, ("two", "Two"): None}}'

    would yield

    'dict_new = {"A": 1, "B": {"One": 1, "Two": 2}}'.
    """
    dict_new = {}

    for key_org, value_org in dict_org.items():

        label_mapper = dict(dict_map.keys())
        try:
            key_new = label_mapper[key_org.lower()]
        except KeyError:
            continue

        if isinstance(value_org, list):
            dict_map_inner = dict_map[(key_org.lower(), key_new)]
            dict_org_inner_list = value_org
            dict_new[key_new] = [
                _dict_rename(dict_org_inner_i, dict_map_inner)
                for dict_org_inner_i in dict_org_inner_list
            ]

        elif isinstance(value_org, dict):
            dict_map_inner = dict_map[(key_org.lower(), key_new)]
            dict_org_inner = value_org
            dict_new[key_new] = _dict_rename(dict_org_inner, dict_map_inner)

        else:
            dict_new[key_new] = dict_org[key_org]
    return dict_new


class JSONSpecialParse:
    def __init__(self, datetime_keys=(), location_keys=(), float_keys=(), int_keys=()):
        self._datetime_keys = [key.lower() for key in datetime_keys]
        self._location_keys = [key.lower() for key in location_keys]

        # Remove when endpoints start returning native values
        self._float_keys = [key.lower() for key in float_keys]
        self._int_keys = [key.lower() for key in int_keys]

    def __call__(self, dct):
        dct_update = {
            key: pd.to_datetime(value)
            for key, value in dct.items()
            if key.lower() in self._datetime_keys
        }
        dct.update(dct_update)

        dct_update = {}
        for key, value in dct.items():
            if key.lower() in self._location_keys:
                try:
                    val1, val2 = value.split("#", 1)
                except (AttributeError, ValueError):
                    dct_update[key] = value
                else:
                    dct_update[key] = (self._float(val1), self._float(val2))
        dct.update(dct_update)

        # Remove when endpoints start returning native values
        dct_update = {
            key: None if value is None else float(value)
            for key, value in dct.items()
            if key.lower() in self._float_keys
        }
        dct.update(dct_update)

        dct_update = {
            key: None if value is None else int(value)
            for key, value in dct.items()
            if key.lower() in self._int_keys
        }
        dct.update(dct_update)
        return dct

    @staticmethod
    def _float(value):
        """
        Attempt to cast "location" string to float. Also converts "null" to ``None``.
        """
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = None if value == "null" else value
        finally:
            return value


json_special_hook = JSONSpecialParse(
    datetime_keys=(
        "start",
        "stop",
        "startdate",
        "enddate",
        "stopdate",
        "attached",
        "detached",
        "dashboardclosedate",
    ),
    location_keys=("location", "geolocation"),
    float_keys=(
        "distancefromwellhead",
        "samplingrate",
        "mass",
        "submergedweight",
        "height",
        "addedmasscoefficient",
        "alpha",
        "waterdepth",
    ),
)


class CampaignsAPI:
    """
    Python wrapper (convenience) for 4Insight Public API - Campaigns.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use ``fourinsight.api.UserSession`` or
        ``fourinsight.api.ClientSession``.
    """

    _API_VERSION = "v1.1"

    def __init__(self, session):
        self._session = session
        self._headers = {
            "user-agent": f"{session.headers['user-agent']} python-fourinsight-campaigns/{fc.__version__}"
        }

    def _url(self, relative_url, api_version=None):
        if api_version is None:
            api_version = self._API_VERSION

        url = f"https://api.4insight.io/{api_version}/Campaigns"
        if relative_url:
            url += f"/{relative_url.lstrip('/')}"
        return url

    def _get_payload(self, url, *args, **kwargs):
        next_link = url
        payload = []
        while next_link:
            response = self._session.get(next_link, headers=self._headers)
            response.raise_for_status()
            json_response = response.json(*args, **kwargs)
            payload.extend(json_response["value"])
            next_link = json_response.get("@odata.nextLink", None)
        return payload

    def _get_payload_legacy(
        self, url, *args, **kwargs
    ):  # remove when v1.1 has all endpoints
        response = self._session.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json(*args, **kwargs)

    def get_campaigns(self):
        """
        Get list of campaigns.

        Parameters
        ----------
        campaign_type : str, optional
            Campaign type ('campaign' or 'swim campaign'). If None, all campaign
            types are returned.

        Returns
        -------
        list of dicts
            A list of campaign dicts.
        """
        response_map = {
            ("id", "CampaignID"): None,
            ("campaignname", "Name"): None,
            ("campaigntype", "Type"): None,
            ("client", "Client"): None,
            ("ponumber", "PO Number"): None,
            ("projectnumber", "Project Number"): None,
            ("vessel", "Vessel"): None,
            ("vesselcontractor", "Vessel Contractor"): None,
            ("wellname", "Well Name"): None,
            ("wellid", "Well ID"): None,
            ("waterdepth", "Water Depth"): None,
            ("location", "Location"): None,
            ("maindataprovider", "Main Data Provider"): None,
            ("startdate", "Start Date"): None,
            ("enddate", "End Date"): None,
            ("geopositionid", "GeoTrack Position ID"): None,
            ("geolocation", "GeoTrack Location"): None,
            ("geotitle", "GeoTrack Title"): None,
            ("hstimeseriesid", "Hs Timeseries ID"): None,
            ("tptimeseriesid", "Tp Timeseries ID"): None,
            ("wdtimeseriesid", "Wd Timeseries ID"): None,
        }

        response = self._get_payload(self._url(""), object_hook=json_special_hook)

        response_out = [
            _dict_rename(campaign_item, response_map) for campaign_item in response
        ]

        return response_out

    def get_campaign(self, campaign_id):
        """
        Get campaign.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Campaign dict.
        """
        response_map = {
            ("id", "CampaignID"): None,
            ("projectnumber", "Project Number"): None,
            ("client", "Client"): None,
            ("vessel", "Vessel"): None,
            ("vesselcontractor", "Vessel Contractor"): None,
            ("wellname", "Well Name"): None,
            ("wellid", "Well ID"): None,
            ("waterdepth", "Water Depth"): None,
            ("location", "Location"): None,
            ("maindataprovider", "Main Data Provider"): None,
            ("startdate", "Start Date"): None,
            ("enddate", "End Date"): None,
        }

        # change to v1.1 when available
        response = self._get_payload_legacy(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook,
        )

        response_out = _dict_rename(response, response_map)
        return response_out

    def get_geotrack(self, campaign_id):
        """
        Get GeoTrack information. (There is no corresponding API endpoint.
        Introduced for consistency and convenience downstream.)

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Campaign dict.
        """
        response_map = {
            ("hstimeseriesid", "HS Timeseries Id"): None,
            ("tptimeseriesid", "Tp Timeseries Id"): None,
            ("wdtimeseriesid", "Wd Timeseries Id"): None,
        }

        # change to v1.1 when available
        response = self._get_payload_legacy(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook,
        )

        response_out = _dict_rename(response, response_map)
        return response_out

    def get_events(self, campaign_id):
        """
        Get events.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Events dict.
        """
        response_map = {
            ("start", "Start"): None,
            ("stop", "End"): None,
            ("eventtype", "Event Type"): None,
            ("comment", "Comment"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Events"), object_hook=json_special_hook
        )

        response_out = [
            _dict_rename(event_item, response_map) for event_item in response
        ]
        return response_out

    def _get_sensors(self, campaign_id):
        """
        Get sensors.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Sensors dict.
        """
        response_map = {
            ("id", "SensorID"): None,
            ("name", "Name"): None,
            ("position", "Position"): None,
            ("distancefromwh", "Distance From Wellhead"): None,
            ("directionxaxis", "Direction X Axis"): None,
            ("directionzaxis", "Direction Z Axis"): None,
            ("samplingrate", "Sampling Rate"): None,
            ("sensorvendor", "Sensor Vendor"): None,
            ("attached", "Attached Time"): None,
            ("detached", "Detached Time"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Sensors"), object_hook=json_special_hook
        )

        response_out = [
            _dict_rename(sensor_item, response_map) for sensor_item in response
        ]
        return response_out

    def _get_channels(self, campaign_id, sensor_id):
        """
        Get sensors channels.

        Parameters
        ----------
        campaign_id : str
            Campaign ID
        sensor_id : str
            Sensor ID

        Returns
        -------
        list
            Channel list.
        """
        response_map = {
            ("name", "Channel"): None,
            ("units", "Units"): None,
            ("timeseriesid", "Timeseries id"): None,
            ("streamid", "Stream id"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Sensors/{sensor_id}/channels"),
            object_hook=json_special_hook,
        )

        response_out = [
            _dict_rename(channel_item, response_map) for channel_item in response
        ]
        return response_out

        return response_out

    def get_sensors(self, campaign_id):
        """
        Get sensors.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Sensors dict.
        """
        sensors = self._get_sensors(campaign_id)
        for sensor in sensors:
            sensor["Channels"] = self._get_channels(campaign_id, sensor["SensorID"])
        return sensors

    def get_lowerstack(self, campaign_id):
        """
        Get lower stack.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Lower stack dict.
        """
        response_map = {
            ("alpha", "Alpha"): None,
            ("elements", "Elements"): {
                ("name", "Name"): None,
                ("mass", "Mass"): None,
                ("submergedweight", "Submerged Weight"): None,
                ("height", "Height"): None,
                ("addedmasscoefficient", "Added Mass Coefficient"): None,
            },
        }

        # change to v1.1 when available
        response = self._get_payload_legacy(
            self._url(f"/{campaign_id}/LowerStack", api_version="v1.0"),
            object_hook=json_special_hook,
        )

        response_out = _dict_rename(response, response_map)
        return response_out

    def get_swimops_campaign(self, campaign_id):
        """
        Get SWIM operations for campaign.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        dict
            Swim operations dict.
        """
        response_map = {
            ("operationstatus", "Operation Status"): None,
            ("dashboardstatus", "Dashboard Status"): None,
            ("slalevel", "SLA Level"): None,
            ("customercontact", "Customer Contact"): None,
            ("comments", "Comments"): None,
            ("dashboardclosedate", "Dashboard Close Date"): None,
            ("swiminstancestatus", "SWIM Instance Status"): None,
            ("reportmade", "Report Made"): None,
            ("reportsent", "Report Sent"): None,
            ("datapackagemade", "Data Package Made"): None,
            ("datapackagesent", "Data Package Sent"): None,
            ("experiencelogMade", "Experience Log Made"): None,
            ("wellspotbendingmomentuploaded", "WellSpot Bending Moment Uploaded"): None,
            ("dashboardclosed", "Dashboard Closed"): None,
            ("servicesavailable", "Services Available"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Swimops"), object_hook=json_special_hook
        )

        response_out = _dict_rename(response[0], response_map)
        return response_out

    def get_swimops(self):
        """
        Get SWIM operations.

        Returns
        -------
        list of dicts
            A list of swim operations dicts.
        """
        response_map = {
            ("operationstatus", "Operation Status"): None,
            ("dashboardstatus", "Dashboard Status"): None,
            ("slalevel", "SLA Level"): None,
            ("customercontact", "Customer Contact"): None,
            ("comments", "Comments"): None,
            ("dashboardclosedate", "Dashboard Close Date"): None,
            ("swiminstancestatus", "SWIM Instance Status"): None,
            ("reportmade", "Report Made"): None,
            ("reportsent", "Report Sent"): None,
            ("datapackagemade", "Data Package Made"): None,
            ("datapackagesent", "Data Package Sent"): None,
            ("experiencelogmade", "Experience Log Made"): None,
            ("wellspotbendingmomentuploaded", "WellSpot Bending Moment Uploaded"): None,
            ("dashboardclosed", "Dashboard Closed"): None,
            ("servicesavailable", "Services Available"): None,
        }

        response = self._get_payload(
            self._url("/Swimops"), object_hook=json_special_hook
        )
        response_out = [
            _dict_rename(swim_ops_item, response_map) for swim_ops_item in response
        ]
        return response_out

    def get_campaign_type(self, campaign_id):
        """
        Get campaign type.

        Parameters
        ----------
        campaign_id : str
            Campaign ID

        Returns
        -------
        str
            Campaign type.
        """
        response_map = {
            ("campaigntype", "CampaignType"): None,
        }
        # change to v1.1 when available
        response = self._get_payload_legacy(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook,
        )
        response = _dict_rename(response, response_map)
        return response["CampaignType"].lower()
