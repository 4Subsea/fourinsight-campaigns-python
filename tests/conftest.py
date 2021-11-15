import json
from unittest.mock import Mock

import pytest
from testdata.get_data import (
    CAMPAIGN_DATA_GENERIC,
    CAMPAIGN_DATA_GENERIC_CAMELCASE,
    CAMPAIGN_DATA_SWIM,
    CAMPAIGN_DATA_SWIM_CAMELCASE,
    CAMPAIGNS_DATA,
    CAMPAIGNS_DATA_CAMELCASE,
    CAMPAIGNS_NEXT_DATA,
    CAMPAIGNS_NEXT_DATA_CAMELCASE,
    CHANNELS_DATA,
    CHANNELS_DATA_CAMELCASE,
    EVENTS_DATA,
    EVENTS_DATA_CAMELCASE,
    LOGS_DATA,
    LOGS_DATA_CAMELCASE,
    LOWERSTACK_DATA,
    LOWERSTACK_DATA_CAMELCASE,
    SENSORS_DATA,
    SENSORS_DATA_CAMELCASE,
    SWIMOPS_CAMPAIGN_DATA,
    SWIMOPS_CAMPAIGN_DATA_CAMELCASE,
    SWIMOPS_DATA,
    SWIMOPS_DATA_CAMELCASE,
)

DATA_MAP = {
    "/v1.1/campaigns": CAMPAIGNS_DATA,
    "campaigns next link": CAMPAIGNS_NEXT_DATA,
    "/v1.1/campaigns/1234/events": EVENTS_DATA,
    "/v1.1/campaigns/1234/sensors": SENSORS_DATA,
    "/v1.0/campaigns/1234/lowerstack": LOWERSTACK_DATA,
    "/v1.1/campaigns/swimops": SWIMOPS_DATA,
    "/v1.1/campaigns/1234/swimops": SWIMOPS_CAMPAIGN_DATA,
    "/v1.1/campaigns/1234/logs": LOGS_DATA,
    "/v1.1/campaigns/1234/sensors/3fa85f64-5717-4562-b3fc-2c963f66afa6/channels": CHANNELS_DATA,
    "/v1.1/campaigns/1234/sensors/<wh sensor id>/channels": CHANNELS_DATA,
    "/v1.0/campaigns/1234": CAMPAIGN_DATA_SWIM,
    "/v1.0/campaigns/test_generic_id": CAMPAIGN_DATA_GENERIC,
    "/v1.0/campaigns/test_swim_id": CAMPAIGN_DATA_SWIM,
}

DATA_MAP_CAMELCASE = {
    "/v1.1/campaigns": CAMPAIGNS_DATA_CAMELCASE,
    "campaigns next link": CAMPAIGNS_NEXT_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/events": EVENTS_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/sensors": SENSORS_DATA_CAMELCASE,
    "/v1.0/campaigns/1234/lowerstack": LOWERSTACK_DATA_CAMELCASE,
    "/v1.1/campaigns/swimops": SWIMOPS_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/swimops": SWIMOPS_CAMPAIGN_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/logs": LOGS_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/sensors/3fa85f64-5717-4562-b3fc-2c963f66afa6/channels": CHANNELS_DATA_CAMELCASE,
    "/v1.1/campaigns/1234/sensors/<wh sensor id>/channels": CHANNELS_DATA_CAMELCASE,
    "/v1.0/campaigns/1234": CAMPAIGN_DATA_SWIM_CAMELCASE,
    "/v1.0/campaigns/test_generic_id": CAMPAIGN_DATA_GENERIC_CAMELCASE,
    "/v1.0/campaigns/test_swim_id": CAMPAIGN_DATA_SWIM_CAMELCASE,
}


@pytest.fixture
def response():
    response = Mock()
    response._get_called_with_url = None

    def json_side_effect(*args, **kwargs):
        url = response._get_called_with_url
        if not url:
            return

        return json.loads(json.dumps(DATA_MAP[url.lower()]), **kwargs)

    response.json.side_effect = json_side_effect
    return response


@pytest.fixture
def response_camelcase():
    response = Mock()
    response._get_called_with_url = None

    def json_side_effect(*args, **kwargs):
        url = response._get_called_with_url
        if not url:
            return

        return json.loads(json.dumps(DATA_MAP_CAMELCASE[url.lower()]), **kwargs)

    response.json.side_effect = json_side_effect
    return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session._api_base_url = "test/api/base/url"

    def get_side_effect(url, *args, **kwargs):
        response._get_called_with_url = url
        return response

    auth_session.get.side_effect = get_side_effect
    return auth_session


@pytest.fixture
def auth_session_camelcase(response_camelcase):
    auth_session = Mock()
    auth_session._api_base_url = "test/api/base/url"

    def get_side_effect(url, *args, **kwargs):
        response_camelcase._get_called_with_url = url
        return response_camelcase

    auth_session.get.side_effect = get_side_effect
    return auth_session
