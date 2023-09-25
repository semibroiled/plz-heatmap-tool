""" This Module will handle any data exploration and modification processes"""


# Data Analysis
import pandas as pd
import numpy as np

# Mapping
from geopy.geocoders import Nominatim

# Type hinting
from pathlib import Path
from pandas import DataFrame, Series

# Local Modules
# moved here

# CI/CD
# from functools import lru_cache
import sys
import os
import logging

# Put Local Module in path
root_directory_module = os.path.abspath(os.path.join(os.path.curdir, "localpack"))
sys.path.append(root_directory_module)

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
fh = logging.FileHandler(f"{__name__}_data.log", mode="a")
fh.setFormatter(formatter)
# fh.setLevel(logging.DEBUG)
log.addHandler(fh)

# Set Logging Level
log.setLevel(logging.DEBUG)


# Initialize Path to Import Files
def declare_filepath(filename: str, extension: str = "csv") -> Path:
    """
    Read specified file from data directory in project code. Return the absolute path
    of this file.

    Args:
        filename (str): _description_
        extension (str, optional): _description_. Defaults to "csv".

    Returns:
        Path: _description_
    """
    current_directory = os.path.dirname(__name__)

    target_directory = os.path.join(current_directory, f"data/{filename}.{extension}")

    abs_path = os.path.abspath(target_directory)

    return abs_path


# Load Data to Python
def load_df(
    filepath: Path,
    col_1: str = "Anmeldedatum",
    col_2: str = "Anmeldezeit",
    delimiter: str = ";",
    is_csv: bool = True,
) -> DataFrame:
    """_summary_

    Args:
        filepath (str): _description_
        col_1 (str, optional): _description_. Defaults to "Anmeldedatum".
        col_2 (str, optional): _description_. Defaults to "Anmeldezeit".
        delimiter (str, optional): _description_. Defaults to ";".
        is_csv (bool, optional): _description_. Defaults to True.

    Returns:
        DataFrame: _description_
    """
    # Load Dataframe
    if is_csv:
        df = pd.read_csv(filepath, delimiter=delimiter, parse_dates=True)

    # Setup Unique ID
    df.loc[:, "Unique_ID"] = (
        df.loc[:, f"{col_1}"]
        .astype(str)
        .str.cat((df.loc[:, f"{col_2}"].astype(str)), sep="_")
    )

    df.index.name = "#ID"

    # Describe Data

    print(df.head())
    print("________________________")
    print(df.tail())
    print("________________________")
    print(df.describe())
    print("========================")

    print(df.isnull().sum())
    print("________________________")
    print(df.isnull().sum().sum())
    print("________________________")
    print(df.isnull().sum().sum())
    print("________________________")

    return df


def transform_df(
    df: DataFrame, set_to_mdz: bool = True, inspect_nans: str = "PLZ"
) -> DataFrame:
    """_summary_

    Args:
        df (DataFrame): _description_
        set_to_mdz (bool, optional): _description_. Defaults to True.
        inspect_nans (str, optional): _description_. Defaults to "PLZ".

    Returns:
        DataFrame: _description_
    """
    if set_to_mdz:
        df = df.loc[:, ["PLZ", "Date"]]
        #! May need to change col to date depending on data entry
        df.dropna(axis=0, subset=[inspect_nans], inplace=True)
        df.loc[:, ["PLZ"]] = df.loc[:, ["PLZ"]].astype(str)

    return df


def init_lat_long(df: DataFrame) -> DataFrame:
    """_summary_

    Args:
        df (DataFrame): _description_

    Returns:
        DataFrame: _description_
    """
    df.loc[:, ["Latitude", "Longitude"]] = np.nan
    return df


# Set Geolocator Instance
geolocator = Nominatim(user_agent="heatmap-tool-mdz")


def my_geocoder(row: Series, zone: str = "DACH", switch: bool = True):
    """_summary_

    Args:
        row (Series): _description_
        zone (str, optional): _description_. Defaults to "DACH".
        switch (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    log.info("Starting my_geocoder function")
    # Setup Coutry Code
    if "dach" in zone.lower():
        log.debug(f"Found {zone}, running zones codes")
        zone_codes = "DE, CH, AT"
    if "euro" in zone.lower():
        log.debug(f"Found {zone}, running zones codes")
        zone_codes = "AT,BE,DE,ES,FI,FR,GR,IE,IT,LU,NL,PT,SI,SK"

    try:
        if switch:
            time.sleep(1.5)

            location = geolocator.geocode(row, country_codes="DE")
            point = location.point

            lat = point.latitude
            long = point.longitude

            address = location.address

            log.info(f"{lat},{long} - {address}")

        else:
            log.debug("Executing try block")
            # Country Codes set to Eurozone or Dach; Set to DACH by Default

            log.debug("Using geolocator to get location")
            location = geolocator.geocode(row, country_codes=zone_codes)
            log.debug("Got location")

            log.debug("Getting location point lat")
            lat = location.point.latitude
            log.debug("Got location point lat")

            log.debug("Getting location point long")
            long = location.point.longitude
            log.debug("Got location point lat")

            log.debug("Getting location address")
            address = location.address
            log.debug("Got location address")

        return {
            "Latitude": lat,
            "Longitude": long,
            "Address": address,
        }

    except ValueError as ve:
        log.error("Registered Error")

        return {
            "Latitude": None,
            "Longitude": None,
            "Address": None,
        }


def add_geocode_data(df: DataFrame, col_to_code: str = "PLZ"):
    """_summary_

    Args:
        df (DataFrame): _description_
        col_to_code (str, optional): _description_. Defaults to "PLZ".

    Returns:
        _type_: _description_
    """
    log.info("Starting function add_geocode_data")
    if col_to_code in df.columns:
        log.debug(f"{col_to_code} found in Columns in Dataframe")
        try:
            log.debug("Executing try block in function")

            try:
                for index, row in df.iterrows():
                    try:
                        log.debug("Executing iteration in function")
                        log.debug(f"Executing {index}th cycle")

                        log.debug("Assign plz value")
                        plz = row[col_to_code]

                        log.debug("Executing my_geocoder in function")
                        geocode_result = my_geocoder(plz)
                        log.debug("Executing my_geocoder for row at columns")

                        log.debug("Executing if block in function")
                        df.at[index, "Latitude"] = geocode_result["Latitude"]
                        log.debug("Append at Index")
                        df.at[index, "Longitude"] = geocode_result["Longitude"]
                        log.debug("Append at index")

                    # df.loc[:, ["Latitude", "Longitude"]] = df.apply(
                    #    lambda x: my_geocoder(x[col_to_code]), axis=1, result_type="expand"
                    # )
                    except:
                        log.error(
                            "Caught exception in try block in iteration and set to pass"
                        )
                        log.debug("Assigning NaN to location")
                        df.at[index, "Latitude"] = np.nan
                        log.debug("Append NaN at Index")
                        df.at[index, "Longitude"] = np.nan
                        log.debug("Append NaN at index")

            except:
                log.error(
                    "Caught exception in try block out of function and set to pass"
                )

        except:
            log.error("Caught exception in try block in function and set to pass")

    else:
        print("The 'PLZ' column does not exist in the DataFrame.")

    # perc_coded = 100 * (1 - ((sum(df.Latitude.isnull().sum())) / len(df)))

    # print(f"{perc_coded}% geocoded in DataFrame")

    return df


def remove_faulty_loc(df: DataFrame) -> DataFrame:
    df.dropna(axis=0, inplace=True)

    return df


def pickle():
    pass


# # Drop universities that were not successfully geocoded
# universities = universities.loc[~np.isnan(universities["Latitude"])]
# universities = gpd.GeoDataFrame(
#     universities,
#     geometry=gpd.points_from_xy(universities.Longitude, universities.Latitude),
# )
# universities.crs = {"init": "epsg:4326"}
# universities.head()

#     return None
