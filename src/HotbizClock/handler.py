from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv

import time
import boto3
import json
import os


def clock(event, context):
    arn = "arn:aws:sns:us-east-1:13XXXXXXXXXX:tty-expired"
    client = boto3.client(
            'sns',
            endpoint_url="http://127.0.0.1:4002",
            region_name="us-east-1"
    )

    # Once a target has expired, we
    # notify our Scraper to GET the
    # latest data points
    expired_targets = __inspect_ttl()

    for e in expired_targets:
        message = json.dumps({
            'default': e
        })
        messageStructure = "json"


        response = client.publish(
                TopicArn = "arn:aws:sns:us-east-1:13XXXXXXXXXX:tty-expired",
                Message=message, 
                MessageStructure=messageStructure
        )

def __inspect_ttl():
    dbClient = __init_db()

    gbfs = dbClient.Table(os.environ.get('GBFS_TABLE', 'gbfs_config'))

    response = gbfs.scan()
    data = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    expired = []

    # Check the timestamp set when we
    # last queried the endpoint.
    # If our current time is more
    # than `ttl` seconds past the
    # previous query time, treat as
    # expired
    for d in data:
        try:
            last_seen = int(d["last_seen"])
        except KeyError:
            last_seen = 0 

        try:
            ttl = int(d["ttl"])
        except KeyError:
            ttl = 0

        try:
            url = d["url"]
        except KeyError:
            # If for some reason we're
            # unable to retrieve the URL
            # there's not much we can do
            # continue and try again later
            continue
        
        current_time = int(time.time())

        # According to the GBFS spec
        # the records shouldn't be updated
        # sooner than `ttl` seconds after
        # the previous update
        if(current_time > last_seen + ttl):
            expired.append(d["url"])

    return expired


def __init_db():
        load_dotenv('./.env')

        endpointUrl = os.environ.get(
                'DYNAMODB_ENDPOINT_URL',
                'http://localhost:8000'
            )
        regionName = os.environ.get(
                'DYNAMO_DB_REGION',
                'localhost'
            )

        dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=endpointUrl,
                region_name=regionName)

        return dynamodb

