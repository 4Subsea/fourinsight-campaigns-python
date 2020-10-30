Basic Usage
###########

Used together with :py:mod:`fourinsight.api` and :py:mod:`datareservoirio`,
:py:mod:`fourinsight.campaigns` makes up an easy-to-use Python interface for
retrieving metadata about campaigns from `4insight.io`_ and download timeseries data
related to a campaign from `DataReservoir.io`_.

Authenticate
------------

To be able to communicate with the 4insight campaigns database, an authenticated session
is required. A User Session can be set up using the
:py:mod:`fourinsight.api` library::

    from fourinsight.api import UserSession
    session = UserSession()
    # Follow instructions to authenticated

.. note::
    For non-interactive applications, consider to use the
    :py:mod:`fourinsight.api.ClientSession` instead. The Client Session does not
    require any user interaction, but expects a ``client_id`` and ``client_secret``
    to be given for authentication. :ref:`Contact us <support>` and we will help you.

To be able to download timeseries data from the DataReservoir, a datareservoir client
must be initiated::

    import datareservoirio as drio
    drio_auth = drio.Authenticator()
    drio_client = drio.Client(drio_auth)

Now you have everything set up to start using the tools provided by
:py:mod:`fourinsight.campaigns`.

Create a client and get campaign data
-------------------------------------

Initiate a campaigns client::

    from fourinsight.campaigns import Client
    client = Client(session)

The campaigns client can be used to get a list of available campaigns in 4insight
using the ``client.overview()`` method, or to get data for a particular campaign
using the ``client.get`` method::

    campaign = client.get('campaign_guid')

Available methods tries to mirror the available tabs in the campaign manager in
4insight.

Display general data in a dict::

    campaign.general()

Get list of events::

    campaign.events()

Get list of sensors::

    campaign.sensors()

It is also possible to filter the list of sensors by position or name. Default
is to filter by position::
    lmrp_sensors = campaign.sensors(value="LMRP", by="Position")

Get sensor data
---------------

Sensor data can be downloaded from the DataReservoir into a pandas.DataFrame using
the ``client.download_sensor_data`` method::

    # Choose which sensor to download from the list of sensors
    sensor = campaign.sensors()[0]
    # Download the sensor data
    campaign.get_sensor_data(drio_client, sensor, filter_=["Ax", "Ay"])

The ``filter_`` argument decides which channels to download. A built-in channel
list is provided by :py:mod:`fourinsight.campaigns.channels`::

    from fourinsight.campaigns import channels
    campaign.get_sensor_data(drio_client, lmrp_sensor, filter_=channels.AG)


.. _4Insight.io: https://4insight.io
.. _DataReservoir.io: https://www.4subsea.com/solutions/digitalisation/datareservoir/
