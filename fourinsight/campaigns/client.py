import warnings

from .campaign import GenericCampaign, SwimCampaign


class Client:
    """
    Client interface for the 4insight.io Campaigns.

    Parameters
    ----------
    session : authorized session
        Authorized session instance which appends a valid bearer token to all
        HTTP calls. Use ``fourinsight.api.UserSession`` or
        ``fourinsight.api.ClientSession``.
    """

    def __init__(self, auth_session):
        self._auth_session = auth_session

    def get(self, campaign_id, campaign_type=None):
        """
        Get the campaign data from the database.

        Parameters
        ----------
        campaign_id : str
            The id of the campaign (GUID).
        campaign_type : str, deprecated.
            Deprecated, but left for backwards compatibility. Type is automatically
            inferred.

        Returns
        -------
        object
            A campaign type specific object containing all relevant information
            about the campaign.
        """
        if campaign_type is not None:
            warnings.warn(
                "Deprecated. Campaign type is automatically inferred. "
                "'campaign_type' keyword will be removed after 1st Jan 2021.")
        CampaignType = self._get_campaign_type(campaign_type)
        return CampaignType(self._auth_session, campaign_id)

    def _get_campaign_type(self, campaign_type):
        campaign_type_map = {"generic": GenericCampaign, "swim": SwimCampaign}
        campaign_type = campaign_type.lower()

        if campaign_type not in campaign_type_map:
            raise ValueError(f'Unknown campaign type "{campaign_type}" given.')
        return campaign_type_map[campaign_type]
