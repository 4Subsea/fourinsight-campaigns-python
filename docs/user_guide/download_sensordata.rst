.. py:currentmodule:: fourinsight.campaigns

Download sensor data
====================

To be able to download timeseries data from the DataReservoir, a :class:`datareservoirio.Client`
must be instantiated:

.. code-block:: python

    import datareservoirio as drio

    drio_auth = drio.Authenticator()
    drio_client = drio.Client(drio_auth)

Sensor data can be downloaded using the :meth:`~GenericCampaign.get_sensor_data` method:

.. code-block:: python

    # Choose which sensor to download from the list of sensors
    sensor = campaign.sensors()[0]

    # Download the sensor data
    campaign.get_sensor_data(drio_client, sensor, filter_=["Ax", "Ay"])

The ``filter_`` keyword argument can be used to filter which channels to download. A built-in channel
list is provided by :mod:`~fourinsight.campaigns.channels` module:

.. code-block:: python

    from fourinsight.campaigns import channels

    campaign.get_sensor_data(drio_client, lmrp_sensor, filter_=channels.AG)

Each sensor has a list of channels which in turn contain Timeseries ids. To access all timeseries that belong to all sensors of a certain campaign (e.g. if needing a list to put them in a timeseries group):

.. code-block:: python

    sensor_list = campaign.sensors()
    timeseries_ids = []

    for item in sensor_list:
        channels = item.get("Channels", [])
        for channel in channels:
            ts_id = channel.get("Timeseries id")
            if ts_id:
                timeseries_ids.append(ts_id)

Or using the ``timeseries`` function:

.. code-block:: python

    timeseries_list = campaign.timeseries()
    timeseries_ids = [
        timeseries['TimeSeriesID']
        for timeseries in timeseries_list
        if timeseries['AttachedTo']['Sensors']
    ]
