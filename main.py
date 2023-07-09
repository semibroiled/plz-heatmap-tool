import logging
import argparse
import pytest

import os, sys, glob

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import geopandas as gpd

import folium
from folium.plugins import HeatMap

from geopy.geocoders import Nominatim

from localpack.handle_data import declare_filepath
from localpack.map_producer import mapper, embed_map

# Put Local Module in path
root_directory_module = os.path.abspath(os.path.join(os.path.curdir, "localpack"))
sys.path.append(root_directory_module)

# Setup Logging Parameters
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

# Setup CLI Parameters

# Setup CLI for calling application from Terminal

# Create Parser Instance
parser = argparse.ArgumentParser()

# Create Subparsers for future functionality
subparser = parser.add_subparsers(dest="command")

# Subparser for fibonacci
heatmap = subparser.add_parser("hm")
# Subparser Greetings
salve_greet = subparser.add_parser("salve")


# Make argument parameters
# Greetings!
salve_greet.add_argument(
    "--echo", type=str, help="Type your name for a customized greeting"
)

# For Heatmap

heatmap.add_argument(
    "--load",
    type=bool,
    required=True,
    default=True,
    help="Read from Savefile",
)
heatmap.add_argument(
    "--radius",
    type=int,
    help="Radius of locations",
)

heatmap.add_argument(
    "--start",
    type=int,
    help="Start Date",
)

heatmap.add_argument(
    "--end",
    type=int,
    help="End Date",
)

heatmap.add_argument(
    "--save",
    type=str,
    help="End Date",
)

args = parser.parse_args()

# Setup Data Cleaning operation on sql entry
# ID According to dates
# Save in a df

# for new rows, settle by id and use preexisitng on duplicate

# Create Heatmap from PLZ

# Save data as pickle,csv or json
# CLI should take subparse of heatmap optional arguments for start and end dates


def main() -> None:
    log.info("Starting Application")

    # Test for successful input of cli args and run app
    try:
        # Run greetings CLI
        if args.command == "salve":
            if args.echo:
                greetings = f"Ily {args.echo} my hobbi!"
                print(greetings)
                log.info(greetings)
            else:
                log.info("No arguments passed")

        # Run Heatmap CLI
        if args.command == "hm":
            # Create Heatmap Flow
            log.info("Creating Maps")

            # Flow 1 - Run from Savefile
            if args.load == True:
                log.info("Load is set to true. Running from savefile")
                log.info("Running Flow 1 - Run from Savefile")
                # Get Filepath
                log.info("Get filepath for pickle")
                savefile = declare_filepath("savefile", extension="pkl")

                # Load Pickle File
                log.info("Load Pickle file")
                saved_df = pd.read_pickle(savefile)

                # Run Mapper
                log.info("Run mapping function")
                m_de = mapper(saved_df)

                # Run Embed Function
                log.info("Get filepath for pickle")
                embed_map(m_de, save_as_image=True)
                log.info("Process Completed!")

            if args.load == False:
                log.warning("Functionality not implemented yet")

                # end = args.upto
                # series = fibonacci(end)

                # print(
                #    f""" Your list of fibonacci numbers upto
                # {end} are:\n {series}"""
                # )
    except ValueError as ve:
        log.error(
            f"Value error. Check that your argument is the right type\
                  \n{ve}"
        )
    except TypeError as te:
        log.error(f"{te}")
    finally:
        pass


if __name__ == "__main__":
    main()
