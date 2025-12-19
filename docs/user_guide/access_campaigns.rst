Accessing campaigns
===================

Authenticate
------------

The first step is to establish a secure connection to the `4insight.io`_ services. This can be achieved
starting a "User Session"::

    from fourinsight.api import UserSession

    session = UserSession()
    # Follow instructions to authenticate

.. note::
    :class:`fourinsight.api.UserSession` is intended for single-user interactive sessions, such
    as coding in notebooks. For non-interactive applications, consider to use the
    :class:`fourinsight.api.ClientSession` instead, which does not
    require any user interaction, but expects ``client_id`` and ``client_secret``.
    ``client_id`` and ``client_secret`` are applications specific credentials that
    are set up on request. :ref:`Contact us <support>` and we will help you.

Now we are ready to proceed.

Retrieve campaign data
----------------------

To initiate a client:

.. code-block:: python

    from fourinsight.campaigns import Client

    client = Client(session)

The client object can be used to get a list of available campaigns in 4insight
using the :meth:`~fourinsight.campaigns.Client.overview()` method::
    
    campaigns = client.overview()

the :meth:`~fourinsight.campaigns.Client.overview()` method returns a dataframe containing all available campaigns and relevant metadata for each, for example campaignID, start time, end time and so on. 
    
To retrieve data for a particular campaign, use the :meth:`~fourinsight.campaigns.Client.get()` method::

    campaign = client.get('campaign_guid')

The ``campaign`` object have methods that "mirror" the sections/tabs in **Campaigns** in `4insight.io`_.

Display general information::

    campaign.general()

Get list of events::

    campaign.events()

Get list of sensors::

    campaign.sensors()

Get list of timeseries::

    campaign.timeseries()

Each timeseries in the list includes general timeseries information, its metadata, and all 4insight connections.

You can use Pandas to visualize the timeseries, connected to the campaign::

    import pandas as pd
    timeseries_list = campaign.timeseries()
    pd.DataFrame(timeseries_list)

To visualize weather timeseries, connected to the campaign::

    import pandas as pd
    timeseries_list = campaign.timeseries()
    weather_timeseries = [
        timeseries
        for timeseries in timeseries_list
        if timeseries["AttachedTo"]["Weather"]
    ]
    pd.DataFrame(weather_timeseries)

To visualize timeseries connections in 4insight::

    import pandas as pd
    timeseries_list = campaign.timeseries()
    connections = [
        timeseries["AttachedTo"]
        for timeseries in timeseries_list
    ]
    pd.DataFrame(connections)

Some methods also support some filtering. For instance, to filter the list of sensors by ``Position``::

    lmrp_sensors = campaign.sensors(value="LMRP", by="Position")

You can also find the timeseries by the corresponding sensor::

    timeseries_list = campaign.timeseries()
    sensor_timeseries = [
        timeseries
        for timeseries in timeseries_list
        if 'sensor_name' in timeseries['AttachedTo']['Sensors']
    ]

.. _4Insight.io: https://4insight.io
.. _DataReservoir.io: https://4subsea.com/products/4insight-data-analytics/
