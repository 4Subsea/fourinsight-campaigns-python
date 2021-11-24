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
        # Make renaming UpperCase / camelCase agnostic.
        key_old = key_old if key_old in dict_org else (key_old[0:1].lower() + key_old[2:])
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
        "Start",
        "stop",
        "Stop",
        "startDate",
        "StartDate",
        "endDate",
        "EndDate",
        "stopDate",
        "StopDate",
        "attached",
        "Attached",
        "detached",
        "Detached",
        "dashboardCloseDate",
        "DashboardCloseDate",
    ),
    location_keys=("location", "Location", "geoLocation", "GeoLocation"),
    float_keys=(
        "distanceFromWellhead",
        "DistanceFromWellhead",
        "samplingRate",
        "SamplingRate",
        "mass",
        "Mass",
        "submergedWeight",
        "SubmergedWeight",
        "height",
        "Height",
        "addedMassCoefficient",
        "AddedMassCoefficient",
        "alpha",
        "Alpha",
        "waterDepth",
        "WaterDepth",
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

    def __init__(self, session):
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
            response = self._session.get(next_link)
            response.raise_for_status()
            json_response = response.json(*args, **kwargs)
            payload.extend(json_response["value"])
            next_link = json_response.get("@odata.nextLink", None)
        return payload

    def _get_payload_legacy(
        self, url, *args, **kwargs
    ):  # remove when v1.1 has all endpoints
        response = self._session.get(url)
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
            ("Id", "CampaignID"): None,
            ("CampaignName", "Name"): None,
            ("CampaignType", "Type"): None,
            ("Client", "Client"): None,
            ("PONumber", "PO Number"): None,
            ("ProjectNumber", "Project Number"): None,
            ("Vessel", "Vessel"): None,
            ("VesselContractor", "Vessel Contractor"): None,
            ("WellName", "Well Name"): None,
            ("WellId", "Well ID"): None,
            ("WaterDepth", "Water Depth"): None,
            ("Location", "Location"): None,
            ("MainDataProvider", "Main Data Provider"): None,
            ("StartDate", "Start Date"): None,
            ("EndDate", "End Date"): None,
            ("GeoPositionId", "GeoTrack Position ID"): None,
            ("GeoLocation", "GeoTrack Location"): None,
            ("GeoTitle", "GeoTrack Title"): None,
            ("HsTimeseriesId", "Hs Timeseries ID"): None,
            ("TpTimeseriesId", "Tp Timeseries ID"): None,
            ("WdTimeseriesId", "Wd Timeseries ID"): None,
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
            ("Id", "CampaignID"): None,
            ("ProjectNumber", "Project Number"): None,
            ("Client", "Client"): None,
            ("Vessel", "Vessel"): None,
            ("VesselContractor", "Vessel Contractor"): None,
            ("WellName", "Well Name"): None,
            ("WellId", "Well ID"): None,
            ("WaterDepth", "Water Depth"): None,
            ("Location", "Location"): None,
            ("MainDataProvider", "Main Data Provider"): None,
            ("StartDate", "Start Date"): None,
            ("EndDate", "End Date"): None,
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
            ("HsTimeseriesId", "HS Timeseries Id"): None,
            ("TpTimeseriesId", "Tp Timeseries Id"): None,
            ("WdTimeseriesId", "Wd Timeseries Id"): None,
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
            ("Start", "Start"): None,
            ("Stop", "End"): None,
            ("EventType", "Event Type"): None,
            ("Comment", "Comment"): None,
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
            ("Id", "SensorID"): None,
            ("Name", "Name"): None,
            ("Position", "Position"): None,
            ("DistanceFromWH", "Distance From Wellhead"): None,
            ("DirectionXAxis", "Direction X Axis"): None,
            ("DirectionZAxis", "Direction Z Axis"): None,
            ("SamplingRate", "Sampling Rate"): None,
            ("SensorVendor", "Sensor Vendor"): None,
            ("Attached", "Attached Time"): None,
            ("Detached", "Detached Time"): None,
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
            ("Name", "Channel"): None,
            ("Units", "Units"): None,
            ("TimeseriesId", "Timeseries id"): None,
            ("StreamId", "Stream id"): None,
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
            ("Alpha", "Alpha"): None,
            ("Elements", "Elements"): {
                ("Name", "Name"): None,
                ("Mass", "Mass"): None,
                ("SubmergedWeight", "Submerged Weight"): None,
                ("Height", "Height"): None,
                ("AddedMassCoefficient", "Added Mass Coefficient"): None,
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
            ("OperationStatus", "Operation Status"): None,
            ("DashboardStatus", "Dashboard Status"): None,
            ("SlaLevel", "SLA Level"): None,
            ("CustomerContact", "Customer Contact"): None,
            ("Comments", "Comments"): None,
            ("DashboardCloseDate", "Dashboard Close Date"): None,
            ("SwimInstanceStatus", "SWIM Instance Status"): None,
            ("ReportMade", "Report Made"): None,
            ("ReportSent", "Report Sent"): None,
            ("DataPackageMade", "Data Package Made"): None,
            ("DataPackageSent", "Data Package Sent"): None,
            ("ExperienceLogMade", "Experience Log Made"): None,
            ("WellSpotBendingMomentUploaded", "WellSpot Bending Moment Uploaded"): None,
            ("DashboardClosed", "Dashboard Closed"): None,
            ("ServicesAvailable", "Services Available"): None,
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
            ("OperationStatus", "Operation Status"): None,
            ("DashboardStatus", "Dashboard Status"): None,
            ("SlaLevel", "SLA Level"): None,
            ("CustomerContact", "Customer Contact"): None,
            ("Comments", "Comments"): None,
            ("DashboardCloseDate", "Dashboard Close Date"): None,
            ("SwimInstanceStatus", "SWIM Instance Status"): None,
            ("ReportMade", "Report Made"): None,
            ("ReportSent", "Report Sent"): None,
            ("DataPackageMade", "Data Package Made"): None,
            ("DataPackageSent", "Data Package Sent"): None,
            ("ExperienceLogMade", "Experience Log Made"): None,
            ("WellSpotBendingMomentUploaded", "WellSpot Bending Moment Uploaded"): None,
            ("DashboardClosed", "Dashboard Closed"): None,
            ("ServicesAvailable", "Services Available"): None,
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
            ("CampaignType", "CampaignType"): None,
        }
        # change to v1.1 when available
        response = self._get_payload_legacy(
            self._url(f"/{campaign_id}", api_version="v1.0"),
            object_hook=json_special_hook,
        )
        response = _dict_rename(response, response_map)
        return response["CampaignType"].lower()
