CAMPAIGNS_DATA_LIST = [
    {
        'id': '6c181d43-0fba-425c-b8bf-06dfb4a661db',
        'campaignName': '1086 - 31/2-F-6',
        'campaignType': 'SWIM Campaign',
        'vessel': 'Songa Endurance',
        'fieldTitle': 'Troll',
        'wellName': '31/2-F-6',
        'startDate': '2017-10-21T00:00:00+00:00'
    }
]


CAMPAIGN_DATA = {
    "id": "028ff3a8-2e08-463d-a4fe-bc10a53450ea",
    "campaignName": "0872 - 30_17a-J4 (P3)",
    "campaignTypeId": "SWIM Campaign",
    "campaignType": "SWIM Campaign",
    "poNumber": None,
    "projectNumber": "0872",
    "client": "Maersk Oil",
    "vesselId": "85719e72-0eaf-43f2-bdd1-2894b735ebd8",
    "vessel": "Ocean Valiant",
    "vesselContractor": "Diamond Offshore",
    "wellName": "Could not fetch well 2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
    "wellId": "2f9356d1-e32c-4916-8f80-bbf8dfaef1e8",
    "fieldTitle": "Janice",
    "waterDepth": None,
    "location": None,
    "mainDataProvider": "4Subsea",
    "startDate": "2017-04-08T00:00:00+00:00",
    "endDate": "2017-05-13T00:00:00+00:00",
    "geoPositionId": "c1092920-0434-483a-ac6b-2511715ab84c",
    "geoLocation": "10#21",
    "geoTitle": "10 er test 2",
    "hsTimeseriesId": "e2ba4833-44ae-4cef-b8a7-18ae82fef327",
    "tpTimeseriesId": "4cfe7e31-f4b5-471f-92c6-b260ee236cff",
    "wdTimeseriesId": "2c6454b8-a274-4845-80e0-cb29c0efc32b",
    "anyFetchFailure": True,
}

EVENTS_DATA = {
    'campaignId': 'string',
    'anyFetchFailure': False,
    'events': [
        {
            'campaignId': 'string',
            'eventType': 'Connect-Disconnect',
            'eventId': 'string',
            'comment': None,
            'startDate': '2020-01-01T00:00:00.0000000Z',
            'stopDate': None
        },
        {
            'campaignId': 'string',
            'eventType': 'Artifact',
            'eventId': 'string',
            'comment': None,
            'startDate': None,
            'stopDate': None
        },
        {
            'campaignId': 'string',
            'eventType': 'WLR connected',
            'eventId': 'string',
            'comment': None,
            'startDate': "2019-01-01T00:00:00.0000000Z",
            'stopDate': None
        },
    ]
}


SENSOR_DATA = {
    'campaignId': '298fbaa3-6ef8-4307-9332-8c32faa7e740',
    'anyFetchFailure': False,
    'sensors': [
        {
            'campaignId': '298fbaa3-6ef8-4307-9332-8c32faa7e740',
            'sensorName': 'SMS0012 - changed',
            'sensorId': '0c65affc-1414-494b-adbe-e75b4f9e49aa',
            'position': '',
            'distanceFromWellhead': '123.45',
            'directionXAxis': 'FWD-PORT',
            'directionZAxis': 'UP',
            'samplingRate': '12',
            'sensorVendor': 'Pulse',
            'attachedTime': '2019-10-13T09:27:19.0000000Z',
            'detachedTime': '2019-10-13T18:07:00.0000000Z',
            'channels': [
                {
                    'sensorId': '0c65affc-1414-494b-adbe-e75b4f9e49aa',
                    'channelName': 'Temp',
                    'channelId': 'a9c1299a-e7cc-4eea-a7ad-94156f4aef20',
                    'units': 'C',
                    'timeseriesId': '1c866249-e03c-4e11-a55b-20de14a031ec',
                    'positionStreamId': 'c4c1fe36-8245-47d2-a10a-be4dd814ccd9'
                }
            ]
        }
    ]
}

LOWERSTACK_DATA = {
    "campaignId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "anyFetchFailure": False,
    "alpha": "string",
    "elements": [
        {
            "campaignId": "string",
            "name": "string",
            "elementId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "mass": "string",
            "submergedWeight": "string",
            "height": "string",
            "addedMassCoefficient": "string"
        }
    ]
}


SWIMOPS_DATA_LIST = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "campaignId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "modified": "2020-10-20T13:12:09.814Z",
        "operationStatus": "string",
        "dashboardStatus": "string",
        "slaLevel": "string",
        "customerContact": "string",
        "comments": "string",
        "dashboardCloseDate": "string",
        "swimInstanceStatus": "string",
        "reportMade": "string",
        "reportSent": "string",
        "dataPackageMade": "string",
        "dataPackageSent": "string",
        "experienceLogMade": "string",
        "wellSpotBendingMomentUploaded": "string",
        "dashboardClosed": "string",
        "servicesAvailable": "string"
    }
]

SWIMOPS_DATA = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "campaignId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "modified": "2020-10-20T13:18:04.726Z",
    "operationStatus": "string",
    "dashboardStatus": "string",
    "slaLevel": "string",
    "customerContact": "string",
    "comments": "string",
    "dashboardCloseDate": "string",
    "swimInstanceStatus": "string",
    "reportMade": "string",
    "reportSent": "string",
    "dataPackageMade": "string",
    "dataPackageSent": "string",
    "experienceLogMade": "string",
    "wellSpotBendingMomentUploaded": "string",
    "dashboardClosed": "string",
    "servicesAvailable": "string"
}
