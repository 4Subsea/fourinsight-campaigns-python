import pandas as pd


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
    for (key_old, key_new), value_map in dict_map.items():
        if value_map is None:
            dict_new[key_new] = dict_org[key_old]
        elif isinstance(value_map, dict):
            value_old = dict_org[key_old]

            if isinstance(value_old, list):
                dict_new[key_new] = [
                    _dict_rename(value_old_i, value_map) for value_old_i in value_old
                ]
            else:
                dict_new[key_new] = _dict_rename(value_old, value_map)
        else:
            raise ValueError("Values in mapping dict must be 'None' or 'dict'")
    return dict_new


class JSONSpecialParse:
    def __init__(self, datetime_keys=(), location_keys=(), float_keys=(), int_keys=()):
        self._datetime_keys = datetime_keys
        self._location_keys = location_keys

        # Remove when endpoints start returning native values
        self._float_keys = float_keys
        self._int_keys = int_keys

    def __call__(self, dct):
        dct_update = {
            key: pd.to_datetime(value)
            for key, value in dct.items()
            if key in self._datetime_keys
        }
        dct.update(dct_update)

        dct_update = {}
        for key, value in dct.items():
            if key in self._location_keys:
                try:
                    val1, val2 = value.split("#")
                except (AttributeError, ValueError):
                    dct_update[key] = value
                else:
                    dct_update[key] = (
                        None if val1 == "null" else float(val1),
                        None if val2 == "null" else float(val2),
                    )
        dct.update(dct_update)

        # Remove when endpoints start returning native values
        dct_update = {
            key: None if value is None else float(value)
            for key, value in dct.items()
            if key in self._float_keys
        }
        dct.update(dct_update)

        dct_update = {
            key: None if value is None else int(value)
            for key, value in dct.items()
            if key in self._int_keys
        }
        dct.update(dct_update)
        return dct


json_special_hook = JSONSpecialParse(
    datetime_keys=(
        "start",
        "stop",
        "startDate",
        "endDate",
        "stopDate",
        # "attachedTime",
        # "detachedTime",
        "attached",
        "detached",
        "dashboardCloseDate",
    ),
    location_keys=("location", "geoLocation"),
    float_keys=(
        "distanceFromWellhead",
        "samplingRate",
        "mass",
        "submergedWeight",
        "height",
        "addedMassCoefficient",
        "alpha",
        "waterDepth",
    ),
)


class CampaignsAPI:
    """
    Python wrapper (convinience) for 4Insight Public API - Campaigns.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use ``fourinsight.api.UserSession`` or
        ``fourinsight.api.ClientSession``.
    """

    _API_VERSION = "v1.1"

    def __init__(self, session, *args, **kwargs):
        self._session = session

    def _url(self, relative_url, api_version=None):
        if api_version is None:
            api_version = self._API_VERSION

        url = f"/{api_version}/Campaigns"
        if relative_url:
            url += f"/{relative_url.lstrip('/')}"
        return url

    def _get_payload(self, url, *args, **kwargs):
        next_link = url
        payload = []
        while next_link:
            json_response = self._session.get(next_link).json(*args, **kwargs)
            payload.extend(json_response["value"])
            next_link = json_response["@odata.nextLink"]
        return payload

    def _get_payload_v10(self, url, *args, **kwargs):   # remove when v1.1 has all endpoints
        return self._session.get(url).json(*args, **kwargs)

    # def _get_method(self, api_version=None):
    #     if api_version is None:
    #         api_version = self._API_VERSION

    #     if api_version.lower() == "v1.0":
    #         return lambda url, *args, **kwargs: self._session.get(url).json(*args, **kwargs)
    #     else:
    #         return self._get_payload

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
            ("campaignName", "Name"): None,
            ("campaignType", "Type"): None,
            ("client", "Client"): None,
            ("poNumber", "PO Number"): None,
            ("projectNumber", "Project Number"): None,
            ("vessel", "Vessel"): None,
            ("vesselContractor", "Vessel Contractor"): None,
            ("wellName", "Well Name"): None,
            ("wellId", "Well ID"): None,
            ("waterDepth", "Water Depth"): None,
            ("location", "Location"): None,
            ("mainDataProvider", "Main Data Provider"): None,
            ("startDate", "Start Date"): None,
            ("endDate", "End Date"): None,
            ("geoPositionId", "GeoTrack Position ID"): None,
            ("geoLocation", "GeoTrack Location"): None,
            ("geoTitle", "GeoTrack Title"): None,
            ("hsTimeseriesId", "Hs Timeseries ID"): None,
            ("tpTimeseriesId", "Tp Timeseries ID"): None,
            ("wdTimeseriesId", "Wd Timeseries ID"): None,
        }

        response = self._get_payload(self._url(""), object_hook=json_special_hook)

        response_out = [
            _dict_rename(campaign_item, response_map)
            for campaign_item in response
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
            ("projectNumber", "Project Number"): None,
            ("client", "Client"): None,
            ("vessel", "Vessel"): None,
            ("vesselContractor", "Vessel Contractor"): None,
            ("wellName", "Well Name"): None,
            ("wellId", "Well ID"): None,
            ("waterDepth", "Water Depth"): None,
            ("location", "Location"): None,
            ("mainDataProvider", "Main Data Provider"): None,
            ("startDate", "Start Date"): None,
            ("endDate", "End Date"): None,
        }

        # change to v1.1 when available
        response = self._get_payload_v10(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook
        )

        response_out = _dict_rename(
            response, response_map
        )
        return response_out

    def get_geotrack(self, campaign_id):
        """
        Get GeoTrack information. (There is no corresponding API endpoint.
        Introduced for consistency and convinience downstream.)

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
            ("hsTimeseriesId", "HS Timeseries Id"): None,
            ("tpTimeseriesId", "Tp Timeseries Id"): None,
            ("wdTimeseriesId", "Wd Timeseries Id"): None,
        }

        # change to v1.1 when available
        response = self._get_payload_v10(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook
        )

        response_out = _dict_rename(
            response, response_map
        )
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
            ("eventType", "Event Type"): None,
            ("comment", "Comment"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Events"),
            object_hook=json_special_hook
        )

        response_out = [
            _dict_rename(event_item, response_map)
            for event_item in response
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
            ("distanceFromWH", "Distance From Wellhead"): None,
            ("directionXAxis", "Direction X Axis"): None,
            ("directionZAxis", "Direction Z Axis"): None,
            ("samplingRate", "Sampling Rate"): None,
            ("sensorVendor", "Sensor Vendor"): None,
            ("attached", "Attached Time"): None,
            ("detached", "Detached Time"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Sensors"),
            object_hook=json_special_hook
        )

        response_out = [
            _dict_rename(sensor_item, response_map)
            for sensor_item in response
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
            ("timeseriesId", "Timeseries id"): None,
            ("streamId", "Stream id"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Sensors/{sensor_id}/channels"),
            object_hook=json_special_hook
        )

        response_out = [
            _dict_rename(channel_item, response_map)
            for channel_item in response
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
                ("submergedWeight", "Submerged Weight"): None,
                ("height", "Height"): None,
                ("addedMassCoefficient", "Added Mass Coefficient"): None,
            },
        }

        # change to v1.1 when available
        response = self._get_payload_v10(
            self._url(f"/{campaign_id}/LowerStack", api_version="v1.0"),
            object_hook=json_special_hook
        )

        response_out = _dict_rename(
            response, response_map
        )
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
            ("operationStatus", "Operation Status"): None,
            ("dashboardStatus", "Dashboard Status"): None,
            ("slaLevel", "SLA Level"): None,
            ("customerContact", "Customer Contact"): None,
            ("comments", "Comments"): None,
            ("dashboardCloseDate", "Dashboard Close Date"): None,
            ("swimInstanceStatus", "SWIM Instance Status"): None,
            ("reportMade", "Report Made"): None,
            ("reportSent", "Report Sent"): None,
            ("dataPackageMade", "Data Package Made"): None,
            ("dataPackageSent", "Data Package Sent"): None,
            ("experienceLogMade", "Experience Log Made"): None,
            ("wellSpotBendingMomentUploaded", "WellSpot Bending Moment Uploaded"): None,
            ("dashboardClosed", "Dashboard Closed"): None,
            ("servicesAvailable", "Services Available"): None,
        }

        response = self._get_payload(
            self._url(f"/{campaign_id}/Swimops"),
            object_hook=json_special_hook
        )

        response_out = _dict_rename(
            response[0], response_map
        )
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
            ("operationStatus", "Operation Status"): None,
            ("dashboardStatus", "Dashboard Status"): None,
            ("slaLevel", "SLA Level"): None,
            ("customerContact", "Customer Contact"): None,
            ("comments", "Comments"): None,
            ("dashboardCloseDate", "Dashboard Close Date"): None,
            ("swimInstanceStatus", "SWIM Instance Status"): None,
            ("reportMade", "Report Made"): None,
            ("reportSent", "Report Sent"): None,
            ("dataPackageMade", "Data Package Made"): None,
            ("dataPackageSent", "Data Package Sent"): None,
            ("experienceLogMade", "Experience Log Made"): None,
            ("wellSpotBendingMomentUploaded", "WellSpot Bending Moment Uploaded"): None,
            ("dashboardClosed", "Dashboard Closed"): None,
            ("servicesAvailable", "Services Available"): None,
        }

        response = self._get_payload(self._url("/Swimops"), object_hook=json_special_hook)
        response_out = [
            _dict_rename(swim_ops_item, response_map)
            for swim_ops_item in response
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
        # change to v1.1 when available
        response = self._get_payload_v10(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook
        )
        return response["campaignType"].lower()
