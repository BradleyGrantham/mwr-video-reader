import os
import re
import datetime
import time
import glob
import json
import subprocess

import click
import cv2
from loguru import logger
from tqdm import tqdm

import mwrvr.ocr
import mwrvr.constants
import mwrvr.textract
import mwrvr.scoreboard


def get_video_size(filename):
    statinfo = os.stat(filename)
    size = statinfo.st_size / (1024 ** 3)
    return size


def get_video_length(filename):
    result = subprocess.Popen(["ffprobe", filename],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    length = [x.decode() for x in result.stdout.readlines() if "Duration" in x.decode()][0]
    length = re.findall('(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)', length)[0]
    length = time.strptime(length, '%H:%M:%S')
    return datetime.timedelta(hours=length.tm_hour,
                              minutes=length.tm_min,
                              seconds=length.tm_sec).total_seconds()


def find_scoreboards(video):
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0

    scoreboards = []

    while video.isOpened():

        _, frame = video.read()
        if frame is None:
            break

        if mwrvr.scoreboard.is_final_scoreboard(frame):

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            scoreboards.append(frame)
            frame_number += 600 * 30
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 600 * 30)

        else:
            if frame_number >= total_frames - (30 * 8):
                frame_number += 1
            else:
                frame_number += 30
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 60)

    video.release()

    return scoreboards


def write_data_to_json(video_file, data):
    """Write data to json file with same naming convention as the video file."""
    json_filename = (video_file
                     .replace("/videos/", "/textract-results/")
                     .replace(".mp4", ".json"))

    with open(json_filename, "w") as f:
        json.dump(data, f)


def get_video_metadata(video_file):
    data = dict()
    video_length = get_video_length(video_file)
    video_size = get_video_size(video_file)

    data["video_size"] = video_size
    data["video_length"] = video_length

    return data

@click.command()
@click.option("--video-directory", default=None)
@click.option("--debug/--no-debug", default=False)
def parse_videos(video_directory, debug):

    if debug:
        logger.info("Debug mode")
        logger.info("If you inputted a video-directory, it will be ignored!")
        video_directory = "../data/videos/tiny/*.mp4"

    elif video_directory is None:
        logger.info("No directory given, using current working directory")
        video_directory = "./*.mp4"

    else:
        video_directory = os.path.join(video_directory, "/*.mp4")

    video_files = glob.glob(video_directory)

    for video_file in tqdm(video_files):

        data = get_video_metadata(video_file)

        vid = cv2.VideoCapture(video_file)

        scoreboards = find_scoreboards(vid)

        scoreboards = [mwrvr.scoreboard.crop_scoreboard(scoreboard)
                       for scoreboard in scoreboards]
        data["responses"] = mwrvr.textract.send_multiple_images(scoreboards)

        write_data_to_json(video_file, data)


if __name__ == "__main__":
    parse_videos()
