"""Module for using the AWS Textract API."""
from collections import namedtuple
from itertools import groupby

import cv2
import boto3
import numpy as np
import pandas as pd
import toml

import mwrvr.ocr
import mwrvr.constants


with open("config.toml") as f:
    TEXTRACT_CONFIG = toml.load(f)

TEXTRACT_CLIENT = boto3.client("textract",
                               **TEXTRACT_CONFIG
                               )

Player = namedtuple('Player', ['name', 'score', 'kills', 'deaths',
                               'plants', 'defuses', 'map', 'top_fragger'])
Word = namedtuple("Word", ['text', 'left', 'top'])


def convert_cv2image_to_bytes(image):
    _, buffer = cv2.imencode('.jpg', image)
    return bytearray(buffer)


def send_image(image):
    image_bytes = convert_cv2image_to_bytes(
        image
    )
    response = TEXTRACT_CLIENT.detect_document_text(
        Document={"Bytes": image_bytes},
    )
    return response


def send_multiple_images(image_list):
    responses = []
    for image in image_list:
        r = mwrvr.textract.send_image(image)
        responses.append(r)

    return responses
