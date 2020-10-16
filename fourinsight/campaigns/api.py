from fourinsight.api.globalsettings import environment


_CAMPAIGN_TYPES = [
    "SWIM Campaign",
    "Campaign",
]


class CampaignsAPI:
    _environment = environment
    
    def __init__(self, auth_session):
        self._auth_session = auth_session
        
    def _get_base_url(self):
        return self._environment.api_base_url
    
    def _verify_type(self, campaign_type):
        if campaign_type in _CAMPAIGN_TYPES:
            return campaign_type
        else:
            raise ValueError("Campaign type {campaign_type} not supported.")
        
    def get_campaigns(self, campaign_type=None):
        if not campaign_type:
            return self._auth_session.get(self._get_base_url() + "/v1.0/Campaigns").json()
        else:
            campaign_type = self._verify_type(campaign_type)
            return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/Type/{campaign_type}").json()
    
    def get_campaign(self, campaign_id):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}").json()
    
    def get_events(self, campaign_id):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Events").json()
    
    def get_sensors(self, campaign_id):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Sensors").json()
    
    def get_lowerstack(self, campaign_id):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/LowerStack").json()
    
    def get_swimops_campaign(self, campaign_id):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/LowerStack").json()
    
    def get_swimops(self):
        return self._auth_session.get(self._get_base_url() + f"/v1.0/Campaigns/Swimops").json()
    
    # def get_swimops(self, campaign_id=None):
    #     if not campaign_id:
    #         return self._get_swimops()
    #     else:
    #         return self._get_swimops_campaign(campaign_id)
        
    def get_campaign_type(self, campaign_id):
        return self.get_campaign(campaign_id)["campaignType"]