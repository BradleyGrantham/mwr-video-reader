"""To be run on the JSON results collected from the parse_videos module."""
import os
import glob
import json

import click
import numpy as np
import pandas as pd
from loguru import logger

import mwrvr.constants
import mwrvr.misc
import mwrvr.textract


desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)

INT_COLUMNS = ["score", "kills", "deaths", "plants", "defuses", "top_fragger"]

COLUMNS = ["name", "map", "score", "kills", "deaths", "plants", "defuses",
                  "number_of_maps", "top_fragger", "zero_bomb"]

PER_MAP_COLUMNS = ["kills_per_map", "deaths_per_map", "plants_per_map",
                   "defuses_per_map", "top_fragger_per_map", "zero_bomb_per_map"]


def find_misspellings(s: str, include_bradlx888_as_ntsfbrad=True):
    s = mwrvr.misc.find_jaantr(s)
    s = mwrvr.misc.find_ntsfbrad(s, include_bradlx888=include_bradlx888_as_ntsfbrad)
    s = mwrvr.misc.find_jakeyy(s)
    s = mwrvr.misc.find_jordanx267(s)
    s = mwrvr.misc.find_bennettar95(s)
    s = mwrvr.misc.find_bradlx888(s)
    return s


@click.command()
@click.option("--json-directory", default=None)
@click.option("--output-path", default=None)
@click.option("--group/--dont-group", default=False)
@click.option("--group-by", default=["name"])
@click.option("--per-map/--no-per-map", default=False)
@click.option("--only-team-members/--not-only-team-members", default=False)
@click.option("--include-bradlx888-as-ntsfbrad/--dont-include-bradlx888-as-ntsfbrad",
              default=True)
@click.option("--debug/--no-debug", default=False)
def parse_json(json_directory, output_path, group, group_by, per_map, only_team_members,
               include_bradlx888_as_ntsfbrad, debug):
    if debug:
        logger.info("Debug mode")
        logger.info("If you inputted a video-directory, it will be ignored!")
        json_directory = "../data/json/tiny/*.json"

    elif json_directory is None:
        logger.info("No directory given, using current working directory")
        json_directory = "./*.json"

    else:
        json_directory = os.path.join(json_directory, "*.json")

    json_paths = glob.glob(json_directory)
    # "/Users/bgrantham/Repos/mwr-video-reader/data/textract-results/all/*.json"

    df = read_json_files(json_paths, include_bradlx888_as_ntsfbrad=include_bradlx888_as_ntsfbrad)

    df[INT_COLUMNS] = df[INT_COLUMNS].astype(np.int32)

    if group:
        df = group_data(df, by=group_by)

    if per_map:
        df = add_per_map(df)

    df = df.sort_values(by="score", ascending=False)

    if only_team_members:
        df = df.query(f"name in {mwrvr.constants.TEAM_MEMBERS}")

    df.to_csv(output_path)


def read_json_files(json_paths, include_bradlx888_as_ntsfbrad=True):
    dfs = []
    for json_path in json_paths:
        with open(json_path) as f:
            r = json.load(f)

        try:
            df = pd.concat([mwrvr.textract.parse_response(response) for response in
                            r["responses"]], sort=False)
        except ValueError as e:
            if str(e) == "No objects to concatenate":
                df = pd.DataFrame()
            else:
                raise e

        df = add_metadata(json_path, r, df)

        dfs.append(df)
    df = pd.concat(dfs, sort=False)

    df["name"] = df["name"].apply(find_misspellings,
                                  include_bradlx888_as_ntsfbrad=include_bradlx888_as_ntsfbrad)

    # a number of games column to act as a count when we do our groupby
    df["number_of_maps"] = 1

    return df


def add_metadata(json_path, response, df):
    video_id = json_path.split("-")[-1].replace(".json", "")
    df["video_id"] = video_id
    df["video_length"] = response["video_length"]
    df["video_size"] = response["video_size"]

    return df


def group_data(df, by=("name")):
    grouped = df[COLUMNS].groupby(by=by).sum().reset_index()

    grouped["K/D"] = grouped["kills"] / grouped["deaths"]

    return grouped


def add_per_map(df):
    for col in PER_MAP_COLUMNS:
        df[col] = df[col.replace("_per_map", "")] / df["number_of_maps"]

    return df


if __name__ == "__main__":
    parse_json()
