from dotenv import load_dotenv

import json
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Hotspot will return a list of the
# most heavily trafficked regions in
# the configured region
def hotspot(event, context):
    # Prepares our database client
    # to read prepared results from 
    # the `hotspots` table
    db = DynamoAccessor("hotspots")

    # User-provided options
    geo = event['queryparameters']['geofence']
    date = event['queryparameters']['date']

    # gather the results
    data = db.get_all("hotspots", 10, date)

    print(data)

    return {
            "statusCode": 200,
            "body": json.dumps(
                data
            ),
            "headers": {
                "Content-Type": "application/json"
            }
    }

class DynamoAccessor():
    def __init__(self, table_name):
        self.db = self.__db_connect()

        self.table = self.__load_table(self.db, table_name)

    def get_all(self, limit: int, date: str) -> []:
        table = self.table

        # return results, ordered by tally,
        # descending
        response = table.query(
            KeyConditionExpression=Key('created_at').eq(date),
            ScanIndexForward=false
        )
        data = response["Items"]

        while "LastEvaluatedKey" in response:
            response = table.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])

        return data

    def get(self, rid: str) -> dict:
        table = self.table

        response = table.get_item(
                Key={
                    id: rid
                }
        )

        return data["Item"]

    def __db_connect(self):
        load_dotenv('./.env')

        # unless we specify otherwise in .env
        # assume that we're connecting to localhost
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


    def __load_table(self, db, tableName):
        table = db.Table(tableName)

        return table
