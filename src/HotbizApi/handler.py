from dotenv import load_dotenv

import json
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

def hotspot(event, context):
    db = DynamoAccessor("hotspots")
    data = db.get_all("hotspots")

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

    def get_all(self, limit: int) -> []:
        table = self.table

        response = table.scan()
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
