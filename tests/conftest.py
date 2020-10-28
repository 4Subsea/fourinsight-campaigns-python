import pytest
from unittest.mock import Mock
from .testdata.get_data import (
    CAMPAIGN_DATA_SWIM,
    CAMPAIGN_DATA_GENERIC,
    CAMPAIGNS_DATA_LIST,
    EVENTS_DATA,
    SENSOR_DATA,
    LOWERSTACK_DATA,
    SWIMOPS_DATA_LIST,
    SWIMOPS_DATA,
)


@pytest.fixture
def response():
    response = Mock()
    response._get_called_with_url = None

    def json_side_effect():
        url = response._get_called_with_url
        if not url:
            return
        elif url.endswith("Campaigns"):
            return CAMPAIGNS_DATA_LIST
        elif url.endswith("Campaigns/Type/SWIM Campaign"):
            return CAMPAIGNS_DATA_LIST
        elif url.endswith("Campaigns/Type/Campaign"):
            return CAMPAIGNS_DATA_LIST
        elif url.endswith("Events"):
            return EVENTS_DATA
        elif url.endswith("Sensors"):
            return SENSOR_DATA
        elif url.endswith("LowerStack"):
            return LOWERSTACK_DATA
        elif url.endswith("/Campaigns/Swimops"):
            return SWIMOPS_DATA_LIST
        elif url.endswith("Swimops") and not url.endswith("/Campaigns/Swimops"):
            return SWIMOPS_DATA
        elif url.endswith("Campaigns/test_swim_id"):
            return CAMPAIGN_DATA_SWIM
        elif url.endswith("Campaigns/test_generic_id"):
            return CAMPAIGN_DATA_GENERIC
        elif url.endswith("Campaigns/1234"):
            return CAMPAIGN_DATA_SWIM
        # elif "Campaigns" in url and not any(
        #     [
        #         url.endswith(tag)
        #         for tag in (
        #             "Campaigns",
        #             "SWIM Campaign",
        #             "Campaign",
        #             "Events",
        #             "Sensors",
        #             "LowerStack",
        #             "Swimops",
        #             "test_swim_id",
        #             "test_generic_id",
        #         )
        #     ]
        # ):
        #     return CAMPAIGN_DATA_SWIM

    response.json.side_effect = json_side_effect
    return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session._api_base_url = "test_url"

    def get_side_effect(url, *args, **kwargs):
        response._get_called_with_url = url
        return response

    auth_session.get.side_effect = get_side_effect
    return auth_session
