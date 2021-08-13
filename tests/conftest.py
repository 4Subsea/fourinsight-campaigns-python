import json
from unittest.mock import Mock

import pytest

# from .testdata.get_data import (
#     CAMPAIGN_DATA_GENERIC,
#     CAMPAIGN_DATA_SWIM,
#     CAMPAIGNS_DATA_LIST,
#     EVENTS_DATA,
#     LOWERSTACK_DATA,
#     SENSOR_DATA,
#     SWIMOPS_DATA,
#     SWIMOPS_DATA_LIST,
# )

from .testdata.get_data_v11 import (
    CAMPAIGNS_DATA,
    CAMPAIGNS_NEXT_DATA,
    EVENTS_DATA,
    SENSORS_DATA,
    LOWERSTACK_DATA,
    SWIMOPS_DATA,
    SWIMOPS_CAMPAIGN_DATA,
    CAMPAIGN_DATA_SWIM,
    CAMPAIGN_DATA_GENERIC,
    CHANNELS_DATA,
    LOGS_DATA,
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
    # "/v1.1/campaigns/1234/sensors/5678/channels": CHANNELS_DATA,
    "/v1.1/campaigns/1234/sensors/sensor_id/channels": CHANNELS_DATA,
    "/v1.1/campaigns/1234/sensors/3fa85f64-5717-4562-b3fc-2c963f66afa6/channels": CHANNELS_DATA,
    "/v1.0/campaigns/1234": CAMPAIGN_DATA_SWIM,
    "/v1.0/campaigns/test_generic_id": CAMPAIGN_DATA_GENERIC,
    "/v1.0/campaigns/test_swim_id": CAMPAIGN_DATA_SWIM,
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


# @pytest.fixture
# def response():
#     response = Mock()
#     response._get_called_with_url = None

#     def json_side_effect(*args, **kwargs):
#         url = response._get_called_with_url
#         if not url:
#             return
#         elif url.endswith("Campaigns"):
#             return json.loads(json.dumps(CAMPAIGNS_DATA), **kwargs)
#         elif url.endswith("campaigns next link"):
#             return json.loads(json.dumps(CAMPAIGNS_NEXT_DATA), **kwargs)
#         # elif url.endswith("Campaigns/Type/SWIM Campaign"):
#         #     return json.loads(json.dumps(CAMPAIGNS_DATA_LIST), **kwargs)
#         # elif url.endswith("Campaigns/Type/Campaign"):
#         #     return json.loads(json.dumps(CAMPAIGNS_DATA_LIST), **kwargs)
#         elif url.lower().endswith("events"):
#             return json.loads(json.dumps(EVENTS_DATA), **kwargs)
#         elif url.lower().endswith("sensors"):
#             return json.loads(json.dumps(SENSORS_DATA), **kwargs)
#         elif url.lower().endswith("lowerstack"):
#             return json.loads(json.dumps(LOWERSTACK_DATA), **kwargs)
#         elif url.lower().endswith("/campaigns/swimops"):
#             return json.loads(json.dumps(SWIMOPS_DATA), **kwargs)
#         elif url.lower().endswith("swimops") and not url.lower().endswith("/campaigns/swimops"):
#             return json.loads(json.dumps(SWIMOPS_CAMPAIGN_DATA), **kwargs)
#         elif url.lower().endswith("campaigns/test_swim_id"):
#             return json.loads(json.dumps(CAMPAIGN_DATA_SWIM), **kwargs)
#         elif url.lower().endswith("campaigns/test_generic_id"):
#             return json.loads(json.dumps(CAMPAIGN_DATA_GENERIC), **kwargs)
#         elif url.lower().endswith("campaigns/1234"):
#             return json.loads(json.dumps(CAMPAIGN_DATA_SWIM), **kwargs)
#         elif url.lower().endswith("channels"):
#             return json.loads(json.dumps(CHANNELS_DATA), **kwargs)
#         elif url.lower().endswith("logs"):
#             return json.loads(json.dumps(LOGS_DATA), **kwargs)

#     response.json.side_effect = json_side_effect
#     return response


@pytest.fixture
def auth_session(response):
    auth_session = Mock()
    auth_session._api_base_url = "test_url"

    def get_side_effect(url, *args, **kwargs):
        response._get_called_with_url = url
        return response

    auth_session.get.side_effect = get_side_effect
    return auth_session
