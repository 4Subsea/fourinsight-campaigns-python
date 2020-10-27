import pandas as pd


def _recast_dict(dict_map, dict_org):
    dict_trans = {}
    for key, value in dict_org.items():
        if key in dict_map:
            trans = dict_map[key][1] or (lambda v: v)
            dict_trans[dict_map[key][0]] = trans(value)
    return dict_trans


_campaigns_short_map = {
    "id": ("CampaignID", str),
    "campaignName": ("Name", str),
    "vessel": ("Vessel", str),
    "fieldTitle": ("Field", str),
    "wellName": ("Well Name", str),
    "startDate": ("Start Date", pd.to_datetime),
}

_campaigns_map = {
    "id": ("CampaignID", str),
    "projectNumber": ("Project Number", str),
    "client": ("Client", str),
    "vessel": ("Vessel", str),
    "vesselContractor": ("Vessel Contractor", str),
    "wellName": ("Well Name", str),
    "wellId": ("Well ID", str),
    "waterDepth": ("Water Depth", lambda x: x if x is None else float(x)),
    "location": ("Location", lambda x: x if x is None else tuple(x.split("#"))),
    "mainDataProvider": ("Main Data Provider", str),
    "startDate": ("Start Date", pd.to_datetime),
    "endDate": ("End Date", pd.to_datetime),
}

_geotrack_map = {
    "hsTimeseriesId": ("HS Timeseries Id", str),
    "tpTimeseriesId": ("Tp Timeseries Id", str),
    "wdTimeseriesId": ("Wd Timeseries Id", str),
}

_event_map = {
    "startDate": ("Start", pd.to_datetime),
    "stopDate": ("End", pd.to_datetime),
    "eventType": ("Event Type", str),
    "comment": ("Comment", str),
}

_channel_map = {
    "channelName": ("Channel", str),
    "units": ("Units", str),
    "timeseriesId": ("Timeseries id", str),
    "positionStreamId": ("Stream id", str),
    }

_sensor_map = {
    "sensorId": ("SensorID", str),
    "sensorName": ("Name", str),
    "position": ("Position", str),
    "distanceFromWellhead": ("Distance From Wellhead", lambda x: x if x is None else float(x)),
    "directionXAxis": ("Direction X Axis", str),
    "directionZAxis": ("Direction Z Axis", str),
    "samplingRate": ("Sampling Rate", lambda x: x if x is None else float(x)),
    "sensorVendor": ("Sensor Vendor", str),
    "attachedTime": ("Attached Time", pd.to_datetime),
    "detachedTime": ("Detached Time", pd.to_datetime),
    "channels": ("Channels", lambda x_list: [_recast_dict(_channel_map, x_i) for x_i in x_list]),
}

_lowerstack_element_map = {
    "name": ("Name", str),
    "mass": ("Mass", lambda x: x if x is None else float(x)),
    "submergedWeight": ("Submerged Weight", lambda x: x if x is None else float(x)),
    "height": ("Height", lambda x: x if x is None else float(x)),
    "addedMassCoefficient": (
        "Added Mass Coefficient",
        lambda x: x if x is None else float(x),
    ),
}

_lowerstack_map = {
    "alpha": ("Alpha", lambda x: x if x is None else float(x)),
    "elements": (
        "Elements",
        lambda x_list: [_recast_dict(_lowerstack_element_map, x_i) for x_i in x_list],
    ),
}

_swim_ops_campaign_map = {
    "operationStatus": ("Operation Status", str),
    "dashboardStatus": ("Dashboard Status", str),
    "slaLevel": ("SLA Level", str),
    "customerContact": ("Customer Contact", str),
    "comments": ("Comments", str),
    "dashboardCloseDate": ("Dashboard Close Date", pd.to_datetime),
    "swimInstanceStatus": ("SWIM Instance Status", str),
    "reportMade": ("Report Made", str),
    "reportSent": ("Report Sent", str),
    "dataPackageMade": ("Data Package Made", str),
    "dataPackageSent": ("Data Package Sent", str),
    "experienceLogMade": ("Experience Log Made", str),
    "wellSpotBendingMomentUploaded": ("WellSpot Bending Moment Uploaded", str),
    "dashboardClosed": ("Dashboard Closed", str),
    "servicesAvailable": ("Services Available", str),
}


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
        return f"/{self._api_version}/Campaigns/{relative_url.lstrip('/')}"

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
        if not campaign_type:
            response = self._session.get(self._url(""))
        elif campaign_type.lower() == "swim":
            response = self._session.get(self._url("/Type/SWIM Campaign/"))
        elif campaign_type.lower() == "generic":
            response = self._session.get(self._url("/Type/Campaign/"))
        else:
            raise ValueError("Unknown 'campaign_type'")

        response_out = [
            _recast_dict(_campaigns_short_map, campaign_item)
            for campaign_item in response.json()
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
        response = self._session.get(self._url(f"/{campaign_id}/"))
        response_out = _recast_dict(_campaigns_map, response.json())
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
        response = self._session.get(self._url(f"/{campaign_id}/"))
        response_out = _recast_dict(_geotrack_map, response.json())
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
        response = self._session.get(self._url(f"/{campaign_id}/Events/"))
        response_out = [
            _recast_dict(_event_map, event_item)
            for event_item in response.json()["events"]
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
        response = self._session.get(self._url(f"/{campaign_id}/Sensors/"))
        response_out = [
            _recast_dict(_sensor_map, event_item)
            for event_item in response.json()["sensors"]
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
        response = self._session.get(self._url(f"/{campaign_id}/LowerStack/"))
        response_out = _recast_dict(_lowerstack_map, response.json())
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
        response = self._session.get(self._url(f"/{campaign_id}/Swimops/"))
        response_out = _recast_dict(_swim_ops_campaign_map, response.json())
        return response_out

    def get_swimops(self):
        """
        Get SWIM operations.

        Returns
        -------
        list of dicts
            A list of swim operations dicts.
        """
        response = self._session.get(self._url(f"/Swimops/"))
        response_out = [
            _recast_dict(_swim_ops_campaign_map, swim_ops_item)
            for swim_ops_item in response.json()
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
        response = self._session.get(self._url(f"/{campaign_id}/"))
        return response.json()["campaignType"].lower()
