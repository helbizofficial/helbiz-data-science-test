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

    message = json.dumps({'default': json.dumps({'key': 'value'})})
    messageStructure = "json"


    response = client.publish(
            TopicArn = "arn:aws:sns:us-east-1:13XXXXXXXXXX:tty-expired",
            Message=message, 
            MessageStructure=messageStructure
    )

    print(response)
