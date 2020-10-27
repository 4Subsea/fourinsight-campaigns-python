"""
Python wrapper (convinience) for 4Insight Public API - Campaigns.
"""


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
        return response.json()

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
        return response.json()

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
        return response.json()

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
        return response.json()

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
        return response.json()

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
        response = self._session.get(self._url(f"/{campaign_id}/Swimops/")
        return response.json()

    def get_swimops(self):
        """
        Get SWIM operations.

        Returns
        -------
        list of dicts
            A list of swim operations dicts.
        """
        response = self._session.get(self._url(f"/Swimops/"))
        return response.json()

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
        return self.get_campaign(campaign_id)["campaignType"].lower()
