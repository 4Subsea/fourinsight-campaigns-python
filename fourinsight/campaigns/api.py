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
        "startDate",
        "endDate",
        "stopDate",
        "attachedTime",
        "detachedTime",
        "dashboardCloseDate",
    ),
    location_keys=("location",),
    float_keys=(
        "distanceFromWellhead",
        "samplingRate",
        "mass",
        "submergedWeight",
        "height",
        "addedMassCoefficient",
        "alpha",
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

    def __init__(self, session, api_version="v1.0"):
        self._session = session
        self._api_version = api_version

    def _url(self, relative_url):
        url = f"/{self._api_version}/Campaigns"
        if relative_url:
            url += f"/{relative_url.lstrip('/')}"
        return url

    def get_campaigns(self, campaign_type=None):
        """
        Get list of campaigns.

        Parameters
        ----------
        campaign_type : str, optional
            Campaign type ['generic', 'swim']. If None, all campaign
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
            ("vessel", "Vessel"): None,
            ("fieldTitle", "Field"): None,
            ("wellName", "Well Name"): None,
            ("startDate", "Start Date"): None,
        }

        if not campaign_type:
            response = self._session.get(self._url(""))
        elif campaign_type.lower() == "swim campaign":
            response = self._session.get(self._url("/Type/SWIM Campaign"))
        elif campaign_type.lower() == "campaign":
            response = self._session.get(self._url("/Type/Campaign"))
        else:
            raise ValueError("Unknown 'campaign_type'")

        response_out = [
            _dict_rename(campaign_item, response_map)
            for campaign_item in response.json(object_hook=json_special_hook)
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

        response = self._session.get(self._url(f"/{campaign_id}"))
        response_out = _dict_rename(
            response.json(object_hook=json_special_hook), response_map
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

        response = self._session.get(self._url(f"/{campaign_id}"))
        response_out = _dict_rename(
            response.json(object_hook=json_special_hook), response_map
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
            ("startDate", "Start"): None,
            ("stopDate", "End"): None,
            ("eventType", "Event Type"): None,
            ("comment", "Comment"): None,
        }
        response = self._session.get(self._url(f"/{campaign_id}/Events"))
        response_out = [
            _dict_rename(event_item, response_map)
            for event_item in response.json(object_hook=json_special_hook)["events"]
        ]
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
        response_map = {
            ("sensorId", "SensorID"): None,
            ("sensorName", "Name"): None,
            ("position", "Position"): None,
            ("distanceFromWellhead", "Distance From Wellhead"): None,
            ("directionXAxis", "Direction X Axis"): None,
            ("directionZAxis", "Direction Z Axis"): None,
            ("samplingRate", "Sampling Rate"): None,
            ("sensorVendor", "Sensor Vendor"): None,
            ("attachedTime", "Attached Time"): None,
            ("detachedTime", "Detached Time"): None,
            ("channels", "Channels"): {
                ("channelName", "Channel"): None,
                ("units", "Units"): None,
                ("timeseriesId", "Timeseries id"): None,
                ("positionStreamId", "Stream id"): None,
            },
        }

        response = self._session.get(self._url(f"/{campaign_id}/Sensors"))
        response_out = [
            _dict_rename(sensor_item, response_map)
            for sensor_item in response.json(object_hook=json_special_hook)["sensors"]
        ]
        return response_out

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
        response = self._session.get(self._url(f"/{campaign_id}/LowerStack"))
        response_out = _dict_rename(
            response.json(object_hook=json_special_hook), response_map
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

        response = self._session.get(self._url(f"/{campaign_id}/Swimops"))
        response_out = _dict_rename(
            response.json(object_hook=json_special_hook), response_map
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

        response = self._session.get(self._url(f"/Swimops"))
        response_out = [
            _dict_rename(swim_ops_item, response_map)
            for swim_ops_item in response.json(object_hook=json_special_hook)
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
        response = self._session.get(self._url(f"/{campaign_id}"))
        return response.json(object_hook=json_special_hook)["campaignType"].lower()
