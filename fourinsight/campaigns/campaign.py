import pandas as pd

from fourinsight.api.globalsettings import environment
from .api import CampaignsAPI

class BaseCampaign:
    """Base class with common methods in all campaigns."""

    def __init__(self, auth_session, campaign_id):
        self._auth_session = auth_session
        self._campaign_id = campaign_id
        self._campaigns_api = CampaignsAPI(auth_session)
        self._campaign = self._campaigns_api.get_campaign(campaign_id)
        self._sensors = self._campaigns_api.get_sensors(campaign_id)
        self._events = self._campaigns_api.get_events(campaign_id)
        self._geotrack = self._campaigns_api.get_geotrack(campaign_id)

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

    # def _get_campaign(self, campaign_id)


class GenericCampaign(BaseCampaign):
    pass

class SwimCampaign(BaseCampaign):
    pass