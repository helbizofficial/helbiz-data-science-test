import requests, logging


def read_data(url_list: list):
    """
    Returns list of lists. Each inner list contains latitude and longitude of vehicle.
    :param url_list: List of urls to read real-time GBFS feeds.
    """
    coords = list()
    for url in url_list:
        try:
            r = requests.get(url)
            # If the response code is OK, process data.
            if r.status_code == 200:
                json_data = r.json()
                lats_and_lons = list()
                data = json_data.get('data', 0)

                if not data:
                    vehciles = json_data['bikes']
                else:
                    vehciles = data['bikes']

                for vehicle in vehciles:
                    latitude = float(vehicle['lat'])
                    longitude = float(vehicle['lon'])
                    lats_and_lons.append([latitude, longitude])
                coords.extend(lats_and_lons)
            else:
                logging.info(f'response to the request is {r.status_code}')
        # If there is a connection error to the url, continue.
        except requests.exceptions.ConnectionError as error:
            logging.info(f'connection error to {url}')
            continue
    # If data is retrieved from the urls, return it.
    if len(coords):
        return coords
    # Else return None
    return None


