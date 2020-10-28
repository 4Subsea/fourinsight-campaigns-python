import pandas as pd


def _recast_dict(dict_map, dict_org):
    """
    Filter and rename keys, and cast items in a dict.
    """
    dict_trans = {}
    for key, value in dict_org.items():
        if key in dict_map:
            trans = dict_map[key][1] or (lambda v: v)
            dict_trans[dict_map[key][0]] = trans(value)
    return dict_trans


_campaigns_short_map = {
    "id": ("CampaignID", lambda x: x if x is None else str(x)),
    "campaignType": ("Type", lambda x: x if x is None else str(x)),
    "campaignName": ("Name", lambda x: x if x is None else str(x)),
    "vessel": ("Vessel", lambda x: x if x is None else str(x)),
    "fieldTitle": ("Field", lambda x: x if x is None else str(x)),
    "wellName": ("Well Name", lambda x: x if x is None else str(x)),
    "startDate": ("Start Date", pd.to_datetime),
}

_campaigns_map = {
    "id": ("CampaignID", lambda x: x if x is None else str(x)),
    "projectNumber": ("Project Number", lambda x: x if x is None else str(x)),
    "client": ("Client", lambda x: x if x is None else str(x)),
    "vessel": ("Vessel", lambda x: x if x is None else str(x)),
    "vesselContractor": ("Vessel Contractor", lambda x: x if x is None else str(x)),
    "wellName": ("Well Name", lambda x: x if x is None else str(x)),
    "wellId": ("Well ID", lambda x: x if x is None else str(x)),
    "waterDepth": ("Water Depth", lambda x: x if x is None else float(x)),
    "location": ("Location", lambda x: x if x is None else tuple(x.split("#"))),
    "mainDataProvider": ("Main Data Provider", lambda x: x if x is None else str(x)),
    "startDate": ("Start Date", pd.to_datetime),
    "endDate": ("End Date", pd.to_datetime),
}

_geotrack_map = {
    "hsTimeseriesId": ("HS Timeseries Id", lambda x: x if x is None else str(x)),
    "tpTimeseriesId": ("Tp Timeseries Id", lambda x: x if x is None else str(x)),
    "wdTimeseriesId": ("Wd Timeseries Id", lambda x: x if x is None else str(x)),
}

_event_map = {
    "startDate": ("Start", pd.to_datetime),
    "stopDate": ("End", pd.to_datetime),
    "eventType": ("Event Type", lambda x: x if x is None else str(x)),
    "comment": ("Comment", lambda x: x if x is None else str(x)),
}

_channel_map = {
    "channelName": ("Channel", lambda x: x if x is None else str(x)),
    "units": ("Units", lambda x: x if x is None else str(x)),
    "timeseriesId": ("Timeseries id", lambda x: x if x is None else str(x)),
    "positionStreamId": ("Stream id", lambda x: x if x is None else str(x)),
    }

_sensor_map = {
    "sensorId": ("SensorID", lambda x: x if x is None else str(x)),
    "sensorName": ("Name", lambda x: x if x is None else str(x)),
    "position": ("Position", lambda x: x if x is None else str(x)),
    "distanceFromWellhead": ("Distance From Wellhead", lambda x: x if x is None else float(x)),
    "directionXAxis": ("Direction X Axis", lambda x: x if x is None else str(x)),
    "directionZAxis": ("Direction Z Axis", lambda x: x if x is None else str(x)),
    "samplingRate": ("Sampling Rate", lambda x: x if x is None else float(x)),
    "sensorVendor": ("Sensor Vendor", lambda x: x if x is None else str(x)),
    "attachedTime": ("Attached Time", pd.to_datetime),
    "detachedTime": ("Detached Time", pd.to_datetime),
    "channels": ("Channels", lambda x_list: [_recast_dict(_channel_map, x_i) for x_i in x_list]),
}

_lowerstack_element_map = {
    "name": ("Name", lambda x: x if x is None else str(x)),
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
    "operationStatus": ("Operation Status", lambda x: x if x is None else str(x)),
    "dashboardStatus": ("Dashboard Status", lambda x: x if x is None else str(x)),
    "slaLevel": ("SLA Level", lambda x: x if x is None else str(x)),
    "customerContact": ("Customer Contact", lambda x: x if x is None else str(x)),
    "comments": ("Comments", lambda x: x if x is None else str(x)),
    "dashboardCloseDate": ("Dashboard Close Date", pd.to_datetime),
    "swimInstanceStatus": ("SWIM Instance Status", lambda x: x if x is None else str(x)),
    "reportMade": ("Report Made", lambda x: x if x is None else str(x)),
    "reportSent": ("Report Sent", lambda x: x if x is None else str(x)),
    "dataPackageMade": ("Data Package Made", lambda x: x if x is None else str(x)),
    "dataPackageSent": ("Data Package Sent", lambda x: x if x is None else str(x)),
    "experienceLogMade": ("Experience Log Made", lambda x: x if x is None else str(x)),
    "wellSpotBendingMomentUploaded": ("WellSpot Bending Moment Uploaded", lambda x: x if x is None else str(x)),
    "dashboardClosed": ("Dashboard Closed", lambda x: x if x is None else str(x)),
    "servicesAvailable": ("Services Available", lambda x: x if x is None else str(x)),
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
        if not campaign_type:
            response = self._session.get(self._url(""))
        elif campaign_type.lower() == "swim campaign":
            response = self._session.get(self._url("/Type/SWIM Campaign"))
        elif campaign_type.lower() == "campaign":
            response = self._session.get(self._url("/Type/Campaign"))
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
        response = self._session.get(self._url(f"/{campaign_id}"))
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
        response = self._session.get(self._url(f"/{campaign_id}"))
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
        response = self._session.get(self._url(f"/{campaign_id}/Events"))
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
        response = self._session.get(self._url(f"/{campaign_id}/Sensors"))
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
        response = self._session.get(self._url(f"/{campaign_id}/LowerStack"))
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
        response = self._session.get(self._url(f"/{campaign_id}/Swimops"))
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
        response = self._session.get(self._url(f"/Swimops"))
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
        response = self._session.get(self._url(f"/{campaign_id}"))
        return response.json()["campaignType"].lower()
