"""To be run on the JSON results collected from the parse_videos module."""
import glob
import json

import numpy as np
import pandas as pd

import mwrvr.misc
import mwrvr.textract


desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)


if __name__ == "__main__":
    json_paths = glob.glob("/Users/bgrantham/Repos/mwr-video-reader/data/textract-results/all/*.json")

    dfs = []

    for json_path in json_paths:
        with open(json_path) as f:
            r = json.load(f)

        try:
            df = pd.concat([mwrvr.textract.parse_response(response) for response in r["responses"]], sort=False)
        except ValueError as e:
            if str(e) == "No objects to concatenate":
                df = pd.DataFrame()
            else:
                raise e

        video_id = json_path.split("-")[-1].replace(".json", "")
        df["video_id"] = video_id
        df["video_length"] = r["video_length"]
        df["video_size"] = r["video_size"]

        dfs.append(df)

    df = pd.concat(dfs, sort=False)

    df["name"] = df["name"].apply(mwrvr.misc.find_jaantr)
    df["name"] = df["name"].apply(mwrvr.misc.find_ntsfbrad)
    df["name"] = df["name"].apply(mwrvr.misc.find_jordanx267)
    df["name"] = df["name"].apply(mwrvr.misc.find_jakeyy)
    df["name"] = df["name"].apply(mwrvr.misc.find_bennettar95)
    df["name"] = df["name"].apply(mwrvr.misc.find_bradlx888)

    # a number of games column to act as a count when we do our groupby
    df["number_of_maps"] = 1

    df[["score", "kills", "deaths", "plants", "defuses", "top_fragger"]] = df[["score", "kills", "deaths", "plants", "defuses", "top_fragger"]].astype(np.int32)

    # grouped = df[["name", "map", "score", "kills", "deaths", "plants", "defuses", "number_of_maps", "top_fragger", "zero_bomb"]].groupby(by=["name", "map"]).sum()
    grouped = df[["name", "score", "kills", "deaths", "plants", "defuses",
                  "number_of_maps", "top_fragger", "zero_bomb"]].groupby(by=["name"]).sum()

    grouped["K/D"] = grouped["kills"] / grouped["deaths"]

    per_map = ["kills_per_map", "deaths_per_map", "plants_per_map", "defuses_per_map", "top_fragger_per_map", "zero_bomb_per_map"]
    for item in per_map:
        grouped[item] = grouped[item.replace("_per_map", "")] / grouped["number_of_maps"]

    print(grouped.sort_values(by="score", ascending=False))

    # grouped.query("name in ['ntsfbrad', 'Jordanx267', 'LazyJakeyy', 'bennettar95', 'JaAnTr']").sort_values(by="score", ascending=False).to_csv("/Users/bgrantham/Repos/mwr-video-reader/data/analyses/v0.0.2-20190709.csv")
    grouped.sort_values( by="score", ascending=False).to_csv(
        "/Users/bgrantham/Repos/mwr-video-reader/data/analyses/v0.0.4-20190709.csv")
