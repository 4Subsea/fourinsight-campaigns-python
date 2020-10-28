from unittest.mock import MagicMock

import pytest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from fourinsight.campaigns.utils import (
    to_dict,
    download_sensor_data
)


class Test_to_dict:
    def test_to_dict(self):
        dict_list = [
            {"Name": "Alpha", "Key1": "Value1", "Key2": "Value2"},
            {"Name": "Beta", "Key1": "Value15", "Key717": "ValueRandom"},
        ]
        expected = {
            "Alpha": {"Key1": "Value1", "Key2": "Value2"},
            "Beta": {"Key1": "Value15", "Key717": "ValueRandom"},
        }
        result = to_dict(dict_list, "Name")
        assert expected == result

    def test_to_dict_duplicate_keys_raises_valueerror(self):
        dict_list = [
            {"Name": "Alpha", "Key1": "Value1", "Key2": "Value2"},
            {"Name": "Alpha", "Key1": "Value15", "Key717": "ValueRandom"},
        ]
        with pytest.raises(ValueError):
            to_dict(dict_list, "Name")


class Test_download_sensor_data:

    @pytest.fixture
    def dummy_data(self):
        index = pd.DatetimeIndex(np.array([1, 2, 3]) * 1e9)
        data = {
            "LMRP": pd.Series([1, 2, 3], index),
            "RISER": pd.Series([5, 6, 7], index),
        }
        return index, data

    def test_download_one_channel(self, dummy_data):
        index, data = dummy_data
        mock_client = MagicMock()
        mock_client.get = MagicMock(
            side_effect=[data["LMRP"], data["RISER"]]
        )
        expected = pd.DataFrame({"LMRP": [1, 2, 3]}, index=index)
        result = download_sensor_data(mock_client, {"LMRP": "abc"})
        assert_frame_equal(expected, result)

    def test_download_two_channels(self, dummy_data):
        index, data = dummy_data
        mock_client = MagicMock()
        mock_client.get = MagicMock(
            side_effect=[data["LMRP"], data["RISER"]]
        )
        expected = pd.DataFrame(
            {"LMRP": [1, 2, 3], "RISER": [5, 6, 7]}, index=index
        )
        result = download_sensor_data(mock_client, {"LMRP": "abc", "RISER": "bcd"})
        assert_frame_equal(expected, result, check_like=True)


if __name__ == "__main__":
    pytest.main()
