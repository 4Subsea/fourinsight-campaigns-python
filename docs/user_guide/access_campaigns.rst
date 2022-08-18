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
using the :meth:`~fourinsight.campaigns.Client.overview()` method, or to retrieve data for a particular campaign
using the :meth:`~fourinsight.campaigns.Client.get()` method::

    campaign = client.get('campaign_guid')

The ``campaign`` object have methods that "mirror" the sections/tabs in **Campaigns** in `4insight.io`_.

Display general information::

    campaign.general()

Get list of events::

    campaign.events()

Get list of sensors::

    campaign.sensors()

Some methods also support some filtering. For instance, to filter the list of sensors by ``Position``::

    lmrp_sensors = campaign.sensors(value="LMRP", by="Position")



.. _4Insight.io: https://4insight.io
.. _DataReservoir.io: https://www.4subsea.com/solutions/digitalisation/datareservoir/
