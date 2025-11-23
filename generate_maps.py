import time

import pandas as pd
from geopy.distance import geodesic
from tqdm import tqdm
from folium.plugins import MarkerCluster
import folium
import imgkit
import argparse

# Dictionary with coordinates of some cities
city_coordinates = {
    'Manchester': (53.4808, -2.2426),
    'WashingtonDC': (38.9072, -77.0369),
    'Glasgow': (55.8642, -4.2518),  # Added Glasgow
    'ElPaso': (31.7619, -106.4850)  # Added El Paso
}


def plot_and_save_map(filtered_file_path: str, city_name: str, output_image_path: str):
    """
    Plot the check-in data on a map and save it as a PNG file.

    Args:
        filtered_file_path (str): Path to the filtered data file.
        city_name (str): Name of the city to center the map on.
        output_image_path (str): Path to save the output image file.

    Returns:
        None
    """
    # Read the filtered data file
    data = pd.read_csv(filtered_file_path, delimiter='\t', header=None,names=['user', 'check-in time', 'latitude', 'longitude', 'location id'])

    if city_name not in city_coordinates:
        raise ValueError(f"City '{city_name}' is not in the list of known cities.")

    city_lat, city_lon = city_coordinates[city_name]

    # Create a map centered on the city
    map_ = folium.Map(location=[city_lat, city_lon], zoom_start=12)

    # Use MarkerCluster to handle a large number of points efficiently
    marker_cluster = MarkerCluster().add_to(map_)

    # Add points to the map
    for idx, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['check-in time']).add_to(marker_cluster)

    # Save the map as an HTML file
    map_.save(output_image_path + ".html")


def main():
    parser = argparse.ArgumentParser(description="Generate map from check-in data.")

    # E.g. -GlasgowGowalla
    parser.add_argument("--input_file", required=True, type=str, help="Path to the input check-ins file.")

    # Glasgow
    parser.add_argument("--city_name", required=True, type=str, help="Name of the city to filter data around.")

    # Output
    parser.add_argument("--output_html", required=True, type=str, help="Path to save the output HTML file.")

    args = parser.parse_args()

    output_file_path = args.output_html

    # Generate and save the map
    plot_and_save_map(args.input_file, args.city_name, output_file_path)


if __name__ == "__main__":
    main()
