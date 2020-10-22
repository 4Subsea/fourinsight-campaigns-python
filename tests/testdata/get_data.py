CAMPAIGNS_DATA_LIST = [
    {
        "id": "6c181d43-0fba-425c-b8bf-06dfb4a661db",
        "campaignName": "1086 - 31/2-F-6",
        "campaignType": "SWIM Campaign",
        "vessel": "Songa Endurance",
        "fieldTitle": "Troll",
        "wellName": "31/2-F-6",
        "startDate": "2017-10-21T00:00:00+00:00",
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
    "campaignId": "string",
    "anyFetchFailure": False,
    "events": [
        {
            "campaignId": "string",
            "eventType": "Connect-Disconnect",
            "eventId": "string",
            "comment": None,
            "startDate": "2020-01-01T00:00:00.0000000Z",
            "stopDate": None,
        },
        {
            "campaignId": "string",
            "eventType": "Artifact",
            "eventId": "string",
            "comment": None,
            "startDate": None,
            "stopDate": None,
        },
        {
            "campaignId": "string",
            "eventType": "WLR connected",
            "eventId": "string",
            "comment": None,
            "startDate": "2019-01-01T00:00:00.0000000Z",
            "stopDate": None,
        },
    ],
}


SENSOR_DATA = {
    "campaignId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "anyFetchFailure": False,
    "sensors": [
        {
            "campaignId": "string",
            "sensorName": "SN1234",
            "sensorId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "position": "LMRP",
            "distanceFromWellhead": "string",
            "directionXAxis": "string",
            "directionZAxis": "string",
            "samplingRate": "string",
            "sensorVendor": "string",
            "attachedTime": "2019-10-13T09:27:19.0000000Z",
            "detachedTime": None,
            "channels": [
                {
                    "sensorId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "channelName": "Pitch",
                    "channelId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "units": "string",
                    "timeseriesId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "positionStreamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                }
            ],
        },
        {
            "campaignId": "string",
            "sensorName": "SN5678",
            "sensorId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "position": "WH",
            "distanceFromWellhead": "string",
            "directionXAxis": "string",
            "directionZAxis": "string",
            "samplingRate": "string",
            "sensorVendor": "string",
            "attachedTime": None,
            "detachedTime": None,
            "channels": [
                {
                    "sensorId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "channelName": "Ag",
                    "channelId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "units": "string",
                    "timeseriesId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "positionStreamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                }
            ],
        },
    ],
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
            "addedMassCoefficient": "string",
        }
    ],
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
        "servicesAvailable": "string",
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
    "servicesAvailable": "string",
}
