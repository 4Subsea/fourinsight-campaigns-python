import json
from unittest.mock import Mock

import pytest

from .testdata.get_data import (
    CAMPAIGN_DATA_GENERIC,
    CAMPAIGN_DATA_SWIM,
    CAMPAIGNS_DATA_LIST,
    EVENTS_DATA,
    LOWERSTACK_DATA,
    SENSOR_DATA,
    SWIMOPS_DATA,
    SWIMOPS_DATA_LIST,
)


@pytest.fixture
def response():
    response = Mock()
    response._get_called_with_url = None

    def json_side_effect(*args, **kwargs):
        url = response._get_called_with_url
        if not url:
            return
        elif url.endswith("Campaigns"):
            return json.loads(json.dumps(CAMPAIGNS_DATA_LIST), **kwargs)
        elif url.endswith("Campaigns/Type/SWIM Campaign"):
            return json.loads(json.dumps(CAMPAIGNS_DATA_LIST), **kwargs)
        elif url.endswith("Campaigns/Type/Campaign"):
            return json.loads(json.dumps(CAMPAIGNS_DATA_LIST), **kwargs)
        elif url.endswith("Events"):
            return json.loads(json.dumps(EVENTS_DATA), **kwargs)
        elif url.endswith("Sensors"):
            return json.loads(json.dumps(SENSOR_DATA), **kwargs)
        elif url.endswith("LowerStack"):
            return json.loads(json.dumps(LOWERSTACK_DATA), **kwargs)
        elif url.endswith("/Campaigns/Swimops"):
            return json.loads(json.dumps(SWIMOPS_DATA_LIST), **kwargs)
        elif url.endswith("Swimops") and not url.endswith("/Campaigns/Swimops"):
            return json.loads(json.dumps(SWIMOPS_DATA), **kwargs)
        elif url.endswith("Campaigns/test_swim_id"):
            return json.loads(json.dumps(CAMPAIGN_DATA_SWIM), **kwargs)
        elif url.endswith("Campaigns/test_generic_id"):
            return json.loads(json.dumps(CAMPAIGN_DATA_GENERIC), **kwargs)
        elif url.endswith("Campaigns/1234"):
            return json.loads(json.dumps(CAMPAIGN_DATA_SWIM), **kwargs)

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
