Basic Usage
###########

:py:mod:`fourinsight.campaigns` is an easy-to-use Python interface for
accessing Campaigns in `4insight.io`_ and retrieve information about different campaigns.
It also facilitates for downloading timeseries data related to a campaign from `DataReservoir.io`_.

Authenticate
------------

The first step is to establish a secure connection to the `4insight.io`_ services. This can be achieved
starting a "User Session"::

    from fourinsight.api import UserSession
    session = UserSession()
    # Follow instructions to authenticated

.. note::
    `fourinsight.api.UserSession` is intended for single-user interactive sessions, such
    as coding in notebooks. For non-interactive applications, consider to use the
    :py:mod:`fourinsight.api.ClientSession` instead. The Client Session does not
    require any user interaction, but expects ``client_id`` and ``client_secret``.
    ``client_id`` and ``client_secret`` are applications specific credentials that
    are set up on request. :ref:`Contact us <support>` and we will help you.

Now we are ready to proceed.

Create a client and get campaign data
-------------------------------------

Initiate a campaigns client::

    from fourinsight.campaigns import Client
    client = Client(session)

The campaigns client can be used to get a list of available campaigns in 4insight
using the ``client.overview()`` method, or to get data for a particular campaign
using the ``client.get`` method::

    campaign = client.get('campaign_guid')

The ``campaign`` object have methods that "mirror" the sections/tabs in Campaigns in `4insight.io`_.

Display general information::

    campaign.general()

Get list of events::

    campaign.events()

Get list of sensors::

    campaign.sensors()

Some methods also support some filtering. For instance, to filter the list of sensors by ``Position``::

    lmrp_sensors = campaign.sensors(value="LMRP", by="Position")

Get sensor data
---------------

To be able to download timeseries data from the DataReservoir, a ``datareservoir.Client``
must be instanciated::

    import datareservoirio as drio

    drio_auth = drio.Authenticator()
    drio_client = drio.Client(drio_auth)

Sensor data can be downloaded using the ``client.download_sensor_data`` method::

    # Choose which sensor to download from the list of sensors
    sensor = campaign.sensors()[0]

    # Download the sensor data
    campaign.get_sensor_data(drio_client, sensor, filter_=["Ax", "Ay"])

The ``filter_`` keyword argument can be used to filter which channels to download. A built-in channel
list is provided by :py:mod:`fourinsight.campaigns.channels`::

    from fourinsight.campaigns import channels

    campaign.get_sensor_data(drio_client, lmrp_sensor, filter_=channels.AG)


.. _4Insight.io: https://4insight.io
.. _DataReservoir.io: https://www.4subsea.com/solutions/digitalisation/datareservoir/
