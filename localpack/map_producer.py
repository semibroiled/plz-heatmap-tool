"""This module will handle mapping operations"""

# Mapping
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

# Type Hinting
from pathlib import Path
from folium import Map
from pandas import Series, DataFrame
from typing import List

# Data Analysis
# import pandas as pd
# import numpy as np

# CI/CD
import logging
import datetime

# import time

# Setup Module Level Logging for our Running Application

# Set Instance of Logging for file
log = logging.getLogger(__name__)

# Set Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "", "%"
)

# Set Stream Handler instance and add formatter
# This outputs text to the terminal
sh = logging.StreamHandler()
sh.setFormatter(formatter)
# sh.setLevel(logging.DEBUG)
log.addHandler(sh)

# Set Filehandler instance and formatter
# This creates a file where the logged data is stored
# By default, mode is a, encoding is None, delay is False
fh = logging.FileHandler(f"./log/{__name__}_data.log", mode="a")
fh.setFormatter(formatter)
# fh.setLevel(logging.DEBUG)
log.addHandler(fh)

# Set Logging Level
log.setLevel(logging.DEBUG)


def embed_map(
    map: Map,
    filepath: Path = "../plz-heatmap/Maps",
    save_as_image: bool = False,
) -> Map:
    """_summary_

    Args:
        map (Map): _description_
        filepath (Path, optional): _description_. Defaults to "../plz-heatmap/map".
        save_as_image (bool, optional): _description_. Defaults to False.

    Returns:
        Map: _description_
    """
    from IPython.display import IFrame

    # Generate File ID from Current Time
    id = datetime.date.now().strftime("%d_%b_%y")

    # Generate Name for Map Call
    filename = f"{filepath}/{id}"

    # Save map
    map.save(f"{filename}.html")

    if save_as_image:
        map.save(f"{filename}.jpg")

    return IFrame(filename, width="100%", height="500px")


def mapper(
    df: DataFrame,
    de_box: List[int] = [51.1657, 10.4515],
    tile_selection: int = 0,
    auto_zoom: float = 5.4,
    radius: int = 16,
) -> Map:
    """_summary_

    Returns:
        _type_: _description_
    """
    tiles = ["openstreetmap", "cartrodpositron"]

    m = folium.Map(location=de_box, tiles=tiles[tile_selection], zoom_start=auto_zoom)

    HeatMap(data=df[["Latitude", "Longitude"]], radius=radius).add_to(m)

    return m


"""def my_geocoder(row):
    try:
        point = geolocator.geocode(row).point
        return pd.Series({'Latitude': point.latitude, 'Longitude': point.longitude})
    except:
        return None

universities[['Latitude', 'Longitude']] = universities.apply(lambda x: my_geocoder(x['Name']), axis=1)"""
