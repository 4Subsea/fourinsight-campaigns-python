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


def _loc_to_float(value):
    """
    Attempt to cast "location" string to float. Also converts "null" to ``None``.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = None if value == "null" else value
    finally:
        return value


def _location_convert(value):
    try:
        val1, val2 = value.split("#", 1)
    except (AttributeError, ValueError):
        converted_value = value
    else:
        converted_value = (_loc_to_float(val1), _loc_to_float(val2))

    return converted_value


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

        response = self._get_payload(self._url(""))

        location_keys = ["location", "geolocation"]
        for campaign_item in response:
            for key in campaign_item.keys():
                if key.lower() in location_keys:
                    campaign_item[key] = _location_convert(campaign_item[key])

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
        )

        for key in response.keys():
            if key.lower() in "location":
                response[key] = _location_convert(response[key])

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
            self._url(f"/{campaign_id}", api_version="v1.0")
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

        response = self._get_payload(self._url(f"/{campaign_id}/Events"))

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

        response = self._get_payload(self._url(f"/{campaign_id}/Sensors"))

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
            self._url(f"/{campaign_id}/Sensors/{sensor_id}/channels")
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
            self._url(f"/{campaign_id}/LowerStack", api_version="v1.0")
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

        response = self._get_payload(self._url(f"/{campaign_id}/Swimops"))

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

        response = self._get_payload(self._url("/Swimops"))
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
            self._url(f"/{campaign_id}", api_version="v1.0")
        )
        response = _dict_rename(response, response_map)
        return response["CampaignType"].lower()
