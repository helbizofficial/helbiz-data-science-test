from stream_data import read_data
from hexbin_algorithms import gen_bins_with_bin_width, gen_bins_with_polycollection
from datetime import datetime
from pytz import timezone


def get_hotspots(url_list: list, algorithm: str):
    """
    Returns list containing json strings.
    Each json string contains latitude, longitude, count of vehicles and date.
    :param url_list: list of urls to read real-time data.
    :param bin_size: the size of the bins to create.
    :param algorithm: type of algorithm to use. "bins_with_polycollection" or "bins_with_bin_width"
    """
    # Time zone object
    time_zone = timezone('America/New_York')
    now = str(datetime.now(tz=time_zone))
    
    # Read data from GBFS feeds.
    data = read_data(url_list)
    if algorithm == "bins_with_polycollection":
        hex_centers, vehicle_counts = gen_bins_with_polycollection(data)
    else:
        hex_centers, vehicle_counts = gen_bins_with_bin_width(data, 0.006)

    data = []
    for lat_lon, count in zip(hex_centers, vehicle_counts):
        dct = {
            'latitude': str(lat_lon[0]),
            'longitude': str(lat_lon[1]),
            'count': str(count),
            'date': now
        }

        data.append(str(dct))
    return data
