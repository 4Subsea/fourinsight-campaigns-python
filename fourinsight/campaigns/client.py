from .campaign import GenericCampaign, SwimCampaign


class Client:
    """
    Client interface for the 4insight.io campaigns database.

    Parameters
    ----------
    auth_session : subclass of ``requests.session``
        Authorized session instance which appends a valid bearer token to all
        HTTP calls.
    """

    def __init__(self, auth_session):
        self._auth_session = auth_session

    def get(self, campaign_id, campaign_type="generic"):
        """
        Get the campaign data from the database.

        Parameters
        ----------
        campaign_id : str
            The id of the campaign (GUID).
        campaign_type : str, optional
            Campaign type ['generic', 'swim']. Temporary until this is
            automatically inferred.

        Returns
        -------
        object
            A campaign type specific object containing all relevant information
            about the campaign.
        """
        CampaignType = self._get_campaign_type(campaign_type)
        return CampaignType(self._auth_session, campaign_id)

    def _get_campaign_type(self, campaign_type):
        campaign_type_map = {"generic": GenericCampaign, "swim": SwimCampaign}
        campaign_type = campaign_type.lower()

        if campaign_type not in campaign_type_map:
            raise ValueError(f'Unknown campaign type "{campaign_type}" given.')
        return campaign_type_map[campaign_type]
