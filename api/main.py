import os, markdown, json
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
from google.cloud import bigquery
from flask_httpauth import HTTPBasicAuth
from google.oauth2 import service_account


# Get Credentials.
with open('./credentials.json', 'r') as file:
    json_string = json.load(file)
credentials = service_account.Credentials.from_service_account_info(json_string)
project_id = os.getenv('PROJECT_ID')


# Get USER DATA.
with open('./user_data.json', 'r') as file:
    USER_DATA = json.load(file)


def get_db(credentials, project_id):
    # Make client.
    bqclient = bigquery.Client(
        credentials=credentials,
        project=project_id,
    )
    return bqclient


def query_db(query_string):
    # Initialize BigQuery client object.
    client = get_db(credentials, project_id)
    # API request
    query_job = client.query(query_string)
    # Waits for query to finish
    rows = query_job.result()
    # Download query results into list of dictionaries.
    data = list()
    for i in rows:
        dct = {
            'latitude': i[0],
            'longitude': i[1],
            'avg_vehicle_count': i[2]
        }

        data.append(dct)
    return data


def get_last_update_date():
    query_string = """
    SELECT date FROM `real-time-gbfs-feeds.gbfs_feeds.hotspots`
    ORDER BY date DESC
    LIMIT 1
    """
    client = get_db(credentials, project_id)
    # API request
    query_job = client.query(query_string)
    # Waits for query to finish
    rows = query_job.result()
    time = ''
    for i in rows:
        time+=i[0]
    return time


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()


@app.route("/")
def index():
    """Present API documentation"""

    # Open the README file
    with open('./API_docs.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class Hotposts(Resource):
    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('geofence', required=True)
        parser.add_argument('date', required=True)

        # Parse the arguments into an object.
        args = parser.parse_args()
        geofence = args['geofence']
        date = args['date']

        # If date is not a string, return a 400 error.
        if not isinstance(date, str):
            return {'message': 'date must be string', 'data': {}}, 400

        try:
            datetime_obj = datetime.strptime(date, '%Y-%m-%d')

        # If provided dat is not in %Y-%m-%d format return a 400 error
        except ValueError as error:
            return {'message': f"time data '{date}' does not match format '%Y-%m-%d'", 'data': {}}, 400

        query = f"""
        SELECT
        latitude, longitude, AVG(cnt_vehicles) AS avg_num_vehicles
        FROM
        `real-time-gbfs-feeds.gbfs_feeds.hotspots`
        WHERE date LIKE "{date}%"
        GROUP BY latitude, longitude
        ORDER BY AVG(cnt_vehicles) DESC
        """
        # Get data.
        data = query_db(query)
        date_str = get_last_update_date()
        time = date_str.split('.')[0]
        timestamp = int(datetime.timestamp(datetime.strptime(time, '%Y-%m-%d %H:%M:%S')))
        # If there is no data, return a 404 error.
        if not len(data):
            return {'message': 'There is no data in this date', 'data': {}}, 404

        return {'message': 'data retrieved',
                'last_updated': timestamp,
                'data': data}, 200


api.add_resource(Hotposts, '/hotspots')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
