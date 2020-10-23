import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from fourinsight.campaigns.utils import (
    to_dict,
    download_sensor_data,
    get_sensor_channel_keys,
)


class Test_Client(unittest.TestCase):
    def setUp(self):
        pass

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
        self.assertDictEqual(expected, result)

    def test_to_dict_duplicate_keys_raises_valueerror(self):
        dict_list = [
            {"Name": "Alpha", "Key1": "Value1", "Key2": "Value2"},
            {"Name": "Alpha", "Key1": "Value15", "Key717": "ValueRandom"},
        ]
        with self.assertRaises(ValueError):
            to_dict(dict_list, "Name")


class Test_download_sensor_data(unittest.TestCase):
    def setUp(self):
        self.datetimeindex = pd.DatetimeIndex(np.array([1, 2, 3]) * 1e9)
        self.dummy_data = {
            "LMRP": pd.Series([1, 2, 3], self.datetimeindex),
            "RISER": pd.Series([5, 6, 7], self.datetimeindex),
        }

    def test_download_one_channel(self):
        mock_client = MagicMock()
        mock_client.get = MagicMock(
            side_effect=[self.dummy_data["LMRP"], self.dummy_data["RISER"]]
        )
        expected = pd.DataFrame({"LMRP": [1, 2, 3]}, index=self.datetimeindex)
        result = download_sensor_data(mock_client, {"LMRP": "abc"})
        assert_frame_equal(expected, result)

    def test_download_two_channels(self):
        mock_client = MagicMock()
        mock_client.get = MagicMock(
            side_effect=[self.dummy_data["LMRP"], self.dummy_data["RISER"]]
        )
        expected = pd.DataFrame(
            {"LMRP": [1, 2, 3], "RISER": [5, 6, 7]}, index=self.datetimeindex
        )
        result = download_sensor_data(mock_client, {"LMRP": "abc", "RISER": "bcd"})
        assert_frame_equal(expected, result, check_like=True)


class Test_get_sensor_channel_keys(unittest.TestCase):
    def setUp(self):
        self.sensor_channels = [
            {"Channel": "Ax", "Timeseries id": "0001"},
            {"Channel": "Az", "Timeseries id": "0002"},
        ]

    def test_get_sensor_channel_keys(self):
        expected = {"Ax": "0001", "Az": "0002"}
        result = get_sensor_channel_keys(self.sensor_channels)
        self.assertDictEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
