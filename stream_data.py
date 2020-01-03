import requests


def read_data(url_list: list):
    """
    Returns list of lists. Each inner list contains latitude and longitude of vehicle.
    :param url_list: List of urls to read real-time GBFS feeds.
    """
    coords = list()
    for url in url_list:
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError as error:
            continue

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

    return coords
