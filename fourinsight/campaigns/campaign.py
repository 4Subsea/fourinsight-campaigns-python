import pandas as pd

from fourinsight.api.globalsettings import environment
from .api import CampaignsAPI

class BaseCampaign:
    """Base class with common methods in all campaigns."""

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
        """Get the events by its event type.

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
            return self._events

        events = self._filter_dict_value_by(self._events, value, by)
        if len(events) == 0:
            raise RuntimeError("No events matches the criteria.")

        events = sorted(
            events,
            key=lambda x: x["Start"]
            if x["Start"] else pd.to_datetime("1970-01-01T00:00:00+0000")
            )
        return events

    def sensors(self, value=None, by="Position"):
        """Get a sensor by its position or name.

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
        return {new_key: dict_.get(old_key, None) for old_key, new_key in rename_keys.items()}

    def _dict_list_subset(self, dict_list, rename_keys):
        return [self._dict_subset(dict_i, rename_keys) for dict_i in dict_list]


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
        return self._dict_subset(self._campaigns_api.get_campaign(campaign_id), rename_keys)

    def _get_geotrack(self, campaign_id):
        rename_keys = {
            "hsTimeseriesId": "HS Timeseries Id",
            "tpTimeseriesId": "Tp Timeseries Id",
            "wdTimeseriesId": "Wd Timeseries Id",
        }
        return self._dict_subset(self._campaigns_api.get_campaign(campaign_id), rename_keys)

    def _get_events(self, campaign_id):
        rename_keys = {
            "startDate": "Start",
            "stopDate": "End",
            "eventType": "Event Type",
            "comment": "Comment",
        }
        events = self._dict_list_subset(self._campaigns_api.get_events(campaign_id)["events"], rename_keys)
        for event_i in events:
            event_i["Start"] = pd.to_datetime(event_i.pop("Start"))
            event_i["End"] = pd.to_datetime(event_i.pop("End"))
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
        sensors = self._dict_list_subset(self._campaigns_api.get_sensors(campaign_id)["sensors"], rename_keys_sensors)

        rename_keys_channels = {
            "channelName": "Channel",
            "units": "Units",
            "timeseriesId": "Timeseries id",
            "streamId": "Stream id",
        }
        for sensor in sensors:
            sensor["Channels"] = self._dict_list_subset(sensor["Channels"], rename_keys_channels)
        return sensors


class GenericCampaign(BaseCampaign):
    pass

class SwimCampaign(BaseCampaign):
    pass