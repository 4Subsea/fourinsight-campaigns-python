import pytest
from unittest.mock import Mock, MagicMock
from .testdata.get_data import (
    CAMPAIGN_DATA,
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
    return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session.get.return_value = response
    auth_session._api_base_url = "test_url"
    return auth_session


@pytest.fixture
def response2():
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
        elif "Campaigns" in url and not any(
            [
                url.endswith(tag)
                for tag in (
                    "Campaigns",
                    "SWIM Campaign",
                    "Campaign",
                    "Events",
                    "Sensors",
                    "LowerStack",
                    "Swimops",
                )
            ]
        ):
            return CAMPAIGN_DATA

    response.json.side_effect = json_side_effect
    return response


@pytest.fixture
def auth_session2(response2):
    auth_session = Mock()
    auth_session._api_base_url = "test_url"

    def get_side_effect(url, *args, **kwargs):
        response2._get_called_with_url = url
        return response2
    auth_session.get.side_effect = get_side_effect
    return auth_session
