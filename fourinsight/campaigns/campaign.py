import pandas as pd

from .api import CampaignsAPI
from .utils import download_sensor_data


class GenericCampaign:
    """
    Generic campaign.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use :class:`fourinsight.api.UserSession` or
        :class:`fourinsight.api.ClientSession`.
    campaign_id : str
        The id of the campaign (GUID).
    """

    def __init__(self, session, campaign_id):
        self._campaign_id = campaign_id
        self._campaigns_api = CampaignsAPI(session)

        self._campaign = None
        self._sensors = None
        self._events = None
        self._geotrack = None

    def _lazy_load(self, attr, api_call, args=()):
        if getattr(self, attr) is None:
            setattr(self, attr, api_call(*args))

    def general(self):
        """Get general campaign info."""
        self._lazy_load(
            "_campaign", self._campaigns_api.get_campaign, args=(self._campaign_id,)
        )
        return self._campaign

    def geotrack(self):
        """Get weather (geotrack) information for the campaign."""
        self._lazy_load(
            "_geotrack", self._campaigns_api.get_geotrack, args=(self._campaign_id,)
        )
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
        self._lazy_load(
            "_events", self._campaigns_api.get_events, args=(self._campaign_id,)
        )

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
        self._lazy_load(
            "_sensors", self._campaigns_api.get_sensors, args=(self._campaign_id,)
        )

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

    def get_sensor_data(self, drio_client, source, start=None, end=None, filter_=None):
        """
        Download the sensor data into a DataFrame.

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
        filter_ : list of str, optional
            A list of channel names to include in the results. Common options
            are available in ``fourinsight.campaigns.channels``. Default to None,
            meaning all channels.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the time series for the sensor channels.

        Note
        ----
        You can supply pre-defiend lists from :mod:`fourinsight.campaigns.channels`.
        E.g. ``my_campaign.get_sensor_data(drio_client, lmrp_sensor,
        filter_=fourinsight.campaigns.channels.AG)`` to include all acceleration
        and gyro data.
        """
        if not filter_:

            def cond(channel):
                return True

        else:

            def cond(channel):
                return channel in filter_

        channels = {
            channel["Channel"]: channel["Timeseries id"]
            for channel in source["Channels"]
            if cond(channel["Channel"])
        }

        # switch to walrus operator when possible
        if start is None and not pd.isna(self.general()["Start Date"]):
            start = self.general()["Start Date"]

        if end is None:
            # switch to walrus operator when possible
            if not pd.isna(self.general()["End Date"]):
                end = self.general()["End Date"] + pd.Timedelta("1D")
            else:
                end = "now"

        dataframe = download_sensor_data(drio_client, channels, start=start, end=end)
        return dataframe


class SwimCampaign(GenericCampaign):
    """
    SWIM campaign.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use :class:`fourinsight.api.UserSession` or
        :class:`fourinsight.api.ClientSession`.
    campaign_id : str
        The id of the campaign (GUID).
    """

    def __init__(self, session, campaign_id):
        super().__init__(session, campaign_id)
        self._swim_operations = None
        self._lowerstack = None

    def swim_operations(self):
        """Get the SWIM operation for the campaign."""
        self._lazy_load(
            "_swim_operations",
            self._campaigns_api.get_swimops_campaign,
            args=(self._campaign_id,),
        )
        return self._swim_operations

    def lowerstack(self):
        """Get lowerstack dict."""
        self._lazy_load(
            "_lowerstack",
            self._campaigns_api.get_lowerstack,
            args=(self._campaign_id,),
        )
        return self._lowerstack
