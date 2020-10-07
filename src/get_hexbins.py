import requests
import logging
import matplotlib.pyplot as plt
import numpy as np


# getting the records from the provided url
def get_coordinates(urls:list):
    coordinates = []
    for url in urls:
        try:
            data = requests.get(url).json()
            bikes = data["data"]["bikes"]
            for bike in bikes:
                coordinates.append([float(bike["lat"]), float(bike["lon"])])
        except requests.exceptions.ConnectionError as e:
            logging.error(f'connection error to {url}')
            continue
    return np.array(coordinates)


''' Here: 'coords' is a numpy array '''
def get_hexagon_bins(coords, coordinates:list):
    # x as latitude and y as longitude
    x = coords[:, 0]   
    y = coords[:, 1]
    
    # extent is the limit of the bin which is passed as the list of our [min lat, max lat, min lon, max long]
    # passing linewidths as (0,) divided the map into equal hexbins
    PolyCollection = plt.hexbin(x, y, linewidths=(0,),extent=coordinates)
    plt.close()

    # position of the hexagons centers
    hexagon_centroids = PolyCollection.get_offsets()

    # values of hexagons
    bike_counts = PolyCollection.get_array()

    '''
    here some operations like dropping bike_counts with 0 value,
    sorting it based on decreasing order of bike_counts can be performed
    '''
    return hexagon_centroids, bike_counts










