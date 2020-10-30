Basic Usage
###########

TODO!

Create a client and get campaign data
-------------------------------------

To be able to communicate with the campaigns database, an authenticated session
is required. An authenticated User Session can be set up using the
:py:mod:`fourinsight.api` library::

    from fourinsight.api import UserSession
    session = UserSession()
    # Follow instructions to authenticated

.. note::
    For non-interactive applications, consider to use the
    :py:mod:`fourinsight.api.ClientSession` instead. The Client Session does not
    require any user interaction, but expects a ``client_id`` and ``client_secret``
    to be given for authentication. :ref:`Contact us <support>` and we will help you.

When an authenticated session is available, the campaigns client can be initiated::

    from fourinsight.campaigns import Client
    client = Client(session)

The campaigns client can be used to get a list of available campaigns in 4insight
using the ``client.overview()`` method, or to get data for a particular campaign
using the ```client.get`` method::

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

When working with a campaign it is possible to download all (or some) channels into
a pandas.DataFrame using the ``download_sensor_data`` method::

    sensor = campaign.sensors()[0]   # choose a sensor from the list of sensors
    campaign.get_sensor_data(drio_client, sensor, filter_=["Ax", "Ay"])

You can also use built-in lists provided by :py:mod:`fourinsight.campaigns.channels`::

    from fourinsight.campaigns import channels
    campaign.get_sensor_data(drio_client, lmrp_sensor, filter_=channels.AG)