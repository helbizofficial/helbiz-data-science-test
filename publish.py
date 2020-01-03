import logging
import google.auth
from proc_data import get_hotspots
from os import getenv, environ, getcwd
from google.cloud import pubsub_v1

# Set GOOGLE_APPLICATION_CREDENTIALS environment variable.
environ['GOOGLE_APPLICATION_CREDENTIALS'] = getcwd() + '/credentials.json'

# Explicitly create a credentials object and get Project Id.
credentials, PROJECT_ID = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

# GCP Pub/Sub topic name
TOPIC = getenv('TOPIC')

url_1 = 'https://web.spin.pm/api/gbfs/v1/washington_dc/free_bike_status'
url_2 = 'https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status.json'
url_3 = 'https://data.lime.bike/api/partners/v1/gbfs/arlington/free_bike_status.json'
url_4 = 'https://dc.jumpmobility.com/opendata/free_bike_status.json'
url_5 = 'https://gbfs.bird.co/dc'
url_6 = 'https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/dca/free_bike_status.json'
url_7 = 'https://us-central1-waybots-production.cloudfunctions.net/dcFreeBikeStatus'

# list contains all Washington GBFS feeds.
urls = [url_1, url_2, url_3, url_4, url_5, url_6, url_7]

# Initialize GCP Pub Sub Publisher object.
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)


def publish(publisher, topic, message):
    """
    Publish data into Google Cloud Pub/Sub.
    """
    data = message.encode('utf-8')
    return publisher.publish(topic_path, data=data)


def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            TOPIC, message_future.exception()))
    else:
        print(message_future.result())


def run_job(event, context):
    data = get_hotspots(urls, algorithm='bins_with_polycollection')
    if data:
        for line in data:
            print(line)
            message_future = publish(publisher, topic_path, line)
            message_future.add_done_callback(callback)
    else:
        logging.info('There is no data to process.')
