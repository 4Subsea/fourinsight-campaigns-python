import pandas as pd

from fourinsight.campaigns.api import CampaignsAPI

from .shared import Channels
from .utils import download_sensor_data, get_sensor_channel_keys


class GenericCampaign:
    """
    Generic campaign.

    Parameters
    ----------
    auth_session : subclass of ``requests.session``
        Authorized session instance which appends a valid bearer token to all
        HTTP calls.
    campaign_id : str
        The id of the campaign (GUID).
    """

    def __init__(self, auth_session, campaign_id):
        self._auth_session = auth_session
        self._campaign_id = campaign_id
        self._campaigns_api = CampaignsAPI(auth_session)
        self._campaign = self._get_campaign(campaign_id)
        self._sensors = self._get_sensors(campaign_id)
        self._events = self._get_events(campaign_id)
        self._geotrack = self._get_geotrack(campaign_id)

    def general(self):
        """Get general campaign info."""
        return self._campaign

    def geotrack(self):
        """Get weather (geotrack) information for the campaign."""
        return self._geotrack

    def events(self, value=None, by="Event Type"):
        """
        Get the events by its event type.

        Parameters
        ----------
        value, str (optional)
            The event type to find. If None, return all events.
        by, str
            What to find. Allowed values are `Event Type`.

        Returns
        -------
        list of dicts
            A list containing event dicts. Results are sorted on `Start`.

        """
        if value is None:
            return self._sort_list_by_start(self._events)

        events = self._filter_dict_value_by(self._events, value, by)
        if len(events) == 0:
            raise RuntimeError("No events matches the criteria.")

        return self._sort_list_by_start(events)

    @staticmethod
    def _sort_list_by_start(list_):
        sorted_list = sorted(
            list_,
            key=lambda x: pd.to_datetime(x["Start"])
            if x["Start"]
            else pd.to_datetime(0).tz_localize("UTC"),
        )
        return sorted_list

    def sensors(self, value=None, by="Position"):
        """
        Get a sensor by its position or name.

        Parameters
        ----------
        value, str (optional)
            The position (or name) to find. If None, return all sensors.
        by, str
            What to find. Allowed values are `Position` or `Name`.

        Returns
        -------
        list of dicts
            A list containing sensor dicts.

        """
        if value is None:
            return self._sensors

        sensors = self._filter_dict_value_by(self._sensors, value, by.capitalize())
        if len(sensors) == 0:
            raise RuntimeError("No sensors matches the criteria.")
        return sensors

    @staticmethod
    def _filter_dict_value_by(dict_, value, by):
        return list(filter(lambda x: x[by] == value, dict_))

    @staticmethod
    def _dict_subset(dict_, rename_keys):
        return {new_key: dict_[old_key] for old_key, new_key in rename_keys.items()}

    def _get_campaign(self, campaign_id):
        rename_keys = {
            "id": "CampaignID",
            "projectNumber": "Project Number",
            "client": "Client",
            "vessel": "Vessel",
            "vesselContractor": "Vessel Contractor",
            "wellName": "Well Name",
            "wellId": "Well ID",
            "waterDepth": "Water Depth",
            "location": "Location",
            "mainDataProvider": "Main Data Provider",
            "startDate": "Start Date",
            "endDate": "End Date",
        }
        campaign = self._dict_subset(
            self._campaigns_api.get_campaign(campaign_id), rename_keys
        )
        campaign["Start Date"] = pd.to_datetime(campaign["Start Date"])
        campaign["End Date"] = pd.to_datetime(campaign["End Date"])
        if campaign["Water Depth"] is not None:
            campaign["Water Depth"] = float(campaign["Water Depth"])
        return campaign

    def _get_geotrack(self, campaign_id):
        rename_keys = {
            "hsTimeseriesId": "HS Timeseries Id",
            "tpTimeseriesId": "Tp Timeseries Id",
            "wdTimeseriesId": "Wd Timeseries Id",
        }
        return self._dict_subset(
            self._campaigns_api.get_campaign(campaign_id), rename_keys
        )

    def _get_events(self, campaign_id):
        rename_keys = {
            "startDate": "Start",
            "stopDate": "End",
            "eventType": "Event Type",
            "comment": "Comment",
        }
        events = [
            self._dict_subset(dict_i, rename_keys)
            for dict_i in self._campaigns_api.get_events(campaign_id)["events"]
        ]
        for event_i in events:
            event_i["Start"] = pd.to_datetime(event_i["Start"])
            event_i["End"] = pd.to_datetime(event_i["End"])
        return events

    def _get_sensors(self, campaign_id):
        rename_keys_sensors = {
            "sensorId": "SensorID",
            "sensorName": "Name",
            "position": "Position",
            "distanceFromWellhead": "Distance From Wellhead",
            "directionXAxis": "Direction X Axis",
            "directionZAxis": "Direction Z Axis",
            "samplingRate": "Sampling Rate",
            "sensorVendor": "Sensor Vendor",
            "attachedTime": "Attached Time",
            "detachedTime": "Detached Time",
            "channels": "Channels",
        }
        sensors = [
            self._dict_subset(dict_i, rename_keys_sensors)
            for dict_i in self._campaigns_api.get_sensors(campaign_id)["sensors"]
        ]

        rename_keys_channels = {
            "channelName": "Channel",
            "units": "Units",
            "timeseriesId": "Timeseries id",
            "positionStreamId": "Stream id",
        }
        for sensor in sensors:
            sensor["Channels"] = [
                self._dict_subset(dict_i, rename_keys_channels)
                for dict_i in sensor["Channels"]
            ]

        for sensor in sensors:
            sensor["Attached Time"] = pd.to_datetime(sensor["Attached Time"])
            sensor["Detached Time"] = pd.to_datetime(sensor["Detached Time"])
            if sensor["Distance From Wellhead"] is not None:
                sensor["Distance From Wellhead"] = float(sensor["Distance From Wellhead"])
            if sensor["Sampling Rate"] is not None:
                sensor["Sampling Rate"] = float(sensor["Sampling Rate"])

        return sensors

    def get_sensor_data(
        self, drio_client, source, start=None, end=None, whitelist=None
    ):
        """Download the sensor data into a DataFrame.

        The data will be limited to within the campaign start and end time as
        given in the General section.

        Parameters
        ----------
        drio_client : datareservoirio.Client
            Datareservoirio client instance.
        source : dict
            Source dict. A dict containing a key ``channels`` with a list of
            channel dicts.
        start : str, datetime-like, optional
            start time (inclusive) of the series given as anything pandas.to_datetime
            is able to parse. Default to campaign start date, or 1970-01-01 if not
            given.
        end : str, datetime-like, optional
            stop time (inclusive) of the series given as anything pandas.to_datetime
            is able to parse. Default to campaign end date (inclusive), or now if
            not given.
        whitelist : list of str or campaigns_4s.Channels, optional
            A list of channel names to include in the results. Default to None,
            meaning all channels.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the time series for the sensor channels.

        Note
        ----
        You can supply standard enumerated lists from campaigns_4s.Channels.
        E.g. self.get_sensor_data(drio_client, lmrp_sensor, whitelist=campaigns_4s.Channels.AG)
        to include all acceleration and gyro data.

        """
        channels = get_sensor_channel_keys(source["Channels"])
        if whitelist:
            if isinstance(whitelist, Channels):
                whitelist = whitelist.value
            channels = {k: v for k, v in channels.items() if k in whitelist}

        start = start or self.general()["Start Date"]
        start = start if not pd.isna(start) else 0
        end = end or self.general()["End Date"] + pd.Timedelta("1D")
        end = end if not pd.isna(end) else "now"
        start, end = pd.Timestamp(start), pd.Timestamp(end)

        dataframe = download_sensor_data(drio_client, channels, start=start, end=end)
        return dataframe


class SwimCampaign(GenericCampaign):
    """
    SWIM campaign.

    Parameters
    ----------
    auth_session : subclass of ``requests.session``
        Authorized session instance which appends a valid bearer token to all
        HTTP calls.
    campaign_id : str
        The id of the campaign (GUID).
    """

    def __init__(self, auth_session, campaign_id):
        super().__init__(auth_session, campaign_id)
        self._swim_operations = self._get_swim_operations(campaign_id)

    def swim_operations(self):
        """Get the SWIM operation for the campaign."""
        return self._swim_operations

    def _get_swim_operations(self, campaign_id):
        rename_keys = {
            "operationStatus": "Operation Status",
            "dashboardStatus": "Dashboard Status",
            "slaLevel": "SLA Level",
            "customerContact": "Customer Contact",
            "comments": "Comments",
            "dashboardCloseDate": "Dashboard Close Date",
            "swimInstanceStatus": "SWIM Instance Status",
            "reportMade": "Report Made",
            "reportSent": "Report Sent",
            "dataPackageMade": "Data Package Made",
            "dataPackageSent": "Data Package Sent",
            "experienceLogMade": "Experience Log Made",
            "wellSpotBendingMomentUploaded": "WellSpot Bending Moment Uploaded",
            "dashboardClosed": "Dashboard Closed",
            "servicesAvailable": "Services Available",
        }
        return self._dict_subset(
            self._campaigns_api.get_swimops_campaign(campaign_id), rename_keys
        )


def Campaign(auth_session, campaign_id):
    """
    Interface for getting data from the 4insight.io campaigns database.

    Parameters
    ----------
    auth_session : subclass of ``requests.session``
        Authorized session instance which appends a valid bearer token to all
        HTTP calls.
    campaign_id : str
        The id of the campaign (GUID).

    Returns
    -------
    object
        A campaign type specific object containing all relevant information
        about the campaign.
    """
    campaign_type_map = {"Campaign": GenericCampaign, "SWIM Campaign": SwimCampaign}

    campaign_type = CampaignsAPI(auth_session).get_campaign_type(campaign_id)
    if campaign_type not in campaign_type_map:
        raise NotImplementedError(f'"Campaign type {campaign_type}" is not supported.')

    return campaign_type_map[campaign_type](auth_session, campaign_id)
