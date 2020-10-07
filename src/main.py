import pandas as pd
from datetime import datetime
import os

from get_hexbins import get_coordinates, get_hexagon_bins
from database import get_csv_records


current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
destination_path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), 'output')

# link with the collection of data
github_url = "https://raw.githubusercontent.com/black-tea/swarm-of-scooters/master/data/systems.csv"

#reading only the required columns from the url
df = pd.read_csv(github_url, usecols=['city_name', 'provider', 'gbfs_freebike_url'])

#grabbing all the url of Los Angeles Region and whose provider is not 'jump' (not able to access those data)
urls = [link for link in df[(df['city_name']=='Los Angeles Region') & (df['provider'] != 'jump')]['gbfs_freebike_url']]

#getting the latitude and longitude as np.array
coords = get_coordinates(urls)

#minimum latitude, maximum latitude, minimum longitude, maximum longitude
'''
To find the minimum latitude, maximum latitude, minimum longitude & maximum longitude range of Los Angeles Region
from our data

-->coordinates_range = [np.array(coords).min(0)[0], np.array(coords).max(0)[0],
                        np.array(coords).min(0)[1], np.array(coords).max(0)[1]]
'''

#range of coordinates for LA Region (can be changed to other more precise value if available)
coordinates_range = [33.7063, 34.4062156677246, -118.636191, -117.754280090332]

#using matplotlib.pyplot.hexbin, divide the map into equal hex bins and get bike counts and hexagon_centers
hex_centers, bike_counts = get_hexagon_bins(coords, coordinates_range)

# creating the list of value with desired result to create database and csv file
data = [{'date_and_time': str(current_time),'hexagon_center': str(f'{coords[0]},{coords[1]}'),'num_bikes': num_bikes} \
    for coords, num_bikes in zip(hex_centers, bike_counts)]

# creating database with records for all the iteration and csv file with average_num_bikes after each iteration
get_csv_records(data, destination_path)



