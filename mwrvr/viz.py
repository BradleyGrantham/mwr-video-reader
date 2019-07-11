import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np

import mwrvr.parse_json

PLAYERS = ["ntsfbrad", "Jordanx267", "LazyJakeyy", "bennettar95", "JaAnTr"]

MAPS = ["ALL", "BACKLOT", "CRASH", "DISTRICT", "CROSSFIRE", "STRIKE", "OVERGROWN"]

METRICS = ["K/D", "kills", "score", "deaths", "plants", "defuses", "top_fragger", "kills_per_map", "score_per_map", "deaths_per_map", "plants_per_map", "defuses_per_map"]


def plot_bar(metric, df, game_map, per_map):
    try:
        im = Image.open(f"/Users/bgrantham/Repos/mwr-video-reader/data/images/{game_map.lower()}.webp")
    except FileNotFoundError:
        im = Image.open(
            f"/Users/bgrantham/Repos/mwr-video-reader/data/images/{game_map.lower()}.jpeg")

    if game_map.lower() == "all":
        df = df.groupby(by="name").sum().reset_index()
        df = mwrvr.parse_json.add_per_map(df)
        df = df.sort_values(by=metric, ascending=True)
    else:
        df = df.query(f"map == '{game_map}'").sort_values(by=metric, ascending=True)

    x_labels = df["name"].values
    y = df[metric].values

    x = [(np.array(im).shape[1] / (len(x_labels) + 1)) * i for i in range(1, len(x_labels) + 1)]

    fig, ax1 = plt.subplots()

    ax1.imshow(im, aspect="auto", alpha=1.0)
    ax1.get_yaxis().set_visible(False)
    ax1.set_xlim(0, np.array(im).shape[1])

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis as ax1

    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('exp', color="black")
    ax2.bar(x, y, color="#00dd11", edgecolor="black", alpha=0.8, width=70 if game_map == "STRIKE" else 100)
    ax2.set_xticklabels(x_labels)
    ax2.tick_params(axis='y', labelcolor="black")

    ax2.set_xticks(x)
    ax2.yaxis.tick_left()
    ax2.set_xlim(0, np.array(im).shape[1])

    ax2.set_xticklabels(x_labels)
    plt.setp(ax1.get_xticklabels(), ha="center", rotation=12)

    title = f"{game_map.upper()} - {metric.upper().replace('/', '')}"

    plt.title(title)

    plt.savefig(f"/Users/bgrantham/Repos/mwr-video-reader/data/plots/{title}.png")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(
        "/Users/bgrantham/Repos/mwr-video-reader/data/processed/v0.0.5-20190710.csv",
        index_col=0)
    for metric in METRICS:
        for game_map in MAPS:
            plot_bar(metric, df, game_map, per_map=False)
