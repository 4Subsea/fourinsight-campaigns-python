import pandas as pd

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

    def _get(self, *args, **kwargs):
        response = self._auth_session.get(*args, **kwargs)
        response.raise_for_status()
        return response

    def _dict_subset(self, dict_, rename_keys):
        return {new_key: dict_.get(old_key, None) for old_key, new_key in rename_keys.items()}

    def _dict_list_subset(self, dict_list, rename_keys):
        return [self._dict_subset(dict_i, rename_keys) for dict_i in dict_list]

    def _verify_type(self, campaign_type):
        if campaign_type in _CAMPAIGN_TYPES:
            return campaign_type
        else:
            raise ValueError("Campaign type {campaign_type} not supported.")
        
    def get_campaigns(self, campaign_type=None):
        if not campaign_type:
            return self._get(self._get_base_url() + "/v1.0/Campaigns").json()
        else:
            campaign_type = self._verify_type(campaign_type)
            return self._get(self._get_base_url() + f"/v1.0/Campaigns/Type/{campaign_type}").json()

    def _get_campaign(self, campaign_id):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}").json()

    def get_campaign(self, campaign_id):
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

        return self._dict_subset(self._get_campaign(campaign_id), rename_keys)

    def get_geotrack(self, campaign_id):
        rename_keys = {
            "hsTimeseriesId": "HS Timeseries Id",
            "tpTimeseriesId": "Tp Timeseries Id",
            "wdTimeseriesId": "Wd Timeseries Id",
        }
        return self._dict_subset(self._get_campaign(campaign_id), rename_keys)

    def _get_events(self, campaign_id):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Events").json()

    def get_events(self, campaign_id):
        rename_keys = {
            "startDate": "Start",
            "stopDate": "End",
            "eventType": "Event Type",
            "comment": "Comment",
        }
        events = self._dict_list_subset(self._get_events(campaign_id)["events"], rename_keys)
        for event_i in events:
            event_i["Start"] = pd.to_datetime(event_i.pop("Start"))
            event_i["End"] = pd.to_datetime(event_i.pop("End"))
        return events

    def _get_sensors(self, campaign_id):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/Sensors").json()

    def get_sensors(self, campaign_id):
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
        sensors = self._dict_list_subset(self._get_sensors(campaign_id)["sensors"], rename_keys_sensors)

        rename_keys_channels = {
            "channelName": "Channel",
            "units": "Units",
            "timeseriesId": "Timeseries id",
            "streamId": "Stream id",
        }
        for sensor in sensors:
            sensor["Channels"] = self._dict_list_subset(sensor["Channels"], rename_keys_channels)
        return sensors


    def get_lowerstack(self, campaign_id):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/LowerStack").json()
    
    def get_swimops_campaign(self, campaign_id):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/{campaign_id}/LowerStack").json()
    
    def get_swimops(self):
        return self._get(self._get_base_url() + f"/v1.0/Campaigns/Swimops").json()
    
    # def get_swimops(self, campaign_id=None):
    #     if not campaign_id:
    #         return self._get_swimops()
    #     else:
    #         return self._get_swimops_campaign(campaign_id)
        
    def get_campaign_type(self, campaign_id):
        return self.get_campaign(campaign_id)["campaignType"]   