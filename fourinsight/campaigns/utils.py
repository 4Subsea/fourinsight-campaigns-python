from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd


def to_dict(dict_list, key):
    """Turn any list of dicts into nested dict.

    Take any list of dictionaries and turn them into nested dicts by
    applying the 'key' as the item identifier for each list item instead.

    Parameters
    ----------
    dict_list : list
        A list containing similar dicts. All dicts must contain an item with
        the key equal to the key-argument.
    key : object
        The value of the key on each item will be the identifying key for the
        dict-item replacing the list-item.

    Returns
    -------
    dict
        A nested dict replacing the list of dicts.

    Example
    -------
    Here's an example showing how a list of dicts can be transformed::

        my_list = [
            {'Name': 'Alpha', 'Key1': 'Value1', 'Key2': 'Value2'},
            {'Name': 'Beta', 'Key1': 'Value15', 'Key717': 'ValueRandom'},
        ]

        to_dict(my_list, 'Name')

    Result::

        {
            'Alpha': {'Key1': 'Value1', 'Key2': 'Value2'},
            'Beta': {'Key1': 'Value15', 'Key717': 'ValueRandom'},
        }

    """
    new_dict = {l[key]: {k: v for k, v in l.items() if k not in key} for l in dict_list}

    if len(dict_list) != len(new_dict):
        raise ValueError(f"Duplicate values for key '{key}' isn't allowed.")

    return new_dict


def download_sensor_data(drio_client, channels, start=None, end=None):
    """Download all channels into a pandas.DataFrame.

    Parameters
    ----------
    drio_client : datareservoirio.Client
        The client to use when downloading the data from the Datareservoir.
    channels : dict
        Key-value pairs: channel_name: series_id
    start : str, datetime-like, optional
        start time (inclusive) of the series given as anything pandas.to_datetime
        is able to parse.
    end : str, datetime-like, optional
        stop time (inclusive) of the series given as anything pandas.to_datetime
        is able to parse.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing each channel as a column.

    """
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(drio_client.get, channels[c], start=start, end=end): c
            for c in channels
        }
    data = {futures[f]: f.result() for f in as_completed(futures)}
    df = pd.concat(data, axis=1)

    return df
