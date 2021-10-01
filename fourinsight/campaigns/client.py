import warnings

import pandas as pd

from .api import CampaignsAPI
from .campaign import GenericCampaign, SwimCampaign


class Client:
    """
    Client interface for the 4insight.io Campaigns.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use :class:`fourinsight.api.UserSession` or
        :class:`fourinsight.api.ClientSession`.
    """

    def __init__(self, session):
        self._session = session
        self._campaigns_api = CampaignsAPI(self._session)

    def overview(self):
        """
        Overview of all campaigns. List view.
        """
        response = self._campaigns_api.get_campaigns()
        return pd.DataFrame.from_records(response, index="CampaignID")

    def get(self, campaign_id):
        """
        Get the campaign data from the database.

        Parameters
        ----------
        campaign_id : str
            The id of the campaign (GUID).

        Returns
        -------
        object
            A campaign type specific object containing all relevant information
            about the campaign.
        """

        campaign_type = self._campaigns_api.get_campaign_type(campaign_id)
        Campaign = self._get_campaign_type(campaign_type)
        return Campaign(self._session, campaign_id)

    def _get_campaign_type(self, campaign_type):
        campaign_type = campaign_type.lower()
        campaign_type_map = {"campaign": GenericCampaign, "swim campaign": SwimCampaign}

        if campaign_type not in campaign_type_map:
            warnings.warn(
                f"Unknown campaign type: '{campaign_type}'. Casting as 'generic'."
            )
        return campaign_type_map.get(campaign_type, GenericCampaign)
