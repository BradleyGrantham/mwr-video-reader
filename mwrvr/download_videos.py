import os
import subprocess

from loguru import logger

VIDEO_DIRECTORY = "../data/videos/all/"
VIDEO_NAME_FORMAT = "%(title)s-%(id)s.%(ext)s"
AFTER_DATE = "20161231"
BEFORE_DATE = "20170610"
YOUTUBE_CHANNEL = "https://www.youtube.com/channel/UC4CoROg6eYg_-Q6RpaGFZtg/videos"

cmd = ('youtube-dl '
       f'--output "{os.path.join(VIDEO_DIRECTORY, VIDEO_NAME_FORMAT)}" '
       f'--dateafter {AFTER_DATE} '
       f'--datebefore {BEFORE_DATE} '
       f'{YOUTUBE_CHANNEL}').split()

if __name__ == "__main__":

    if not os.path.exists(VIDEO_DIRECTORY):
        logger.info(f"Creating directory {VIDEO_DIRECTORY}")
        os.makedirs(VIDEO_DIRECTORY)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b""):
        print(line.decode(), end="")
    p.stdout.close()
    p.wait()
