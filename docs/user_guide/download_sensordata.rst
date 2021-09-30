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

