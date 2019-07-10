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
import mwrvr.misc


with open("config.toml") as f:
    TEXTRACT_CONFIG = toml.load(f)

TEXTRACT_CLIENT = boto3.client("textract",
                               **TEXTRACT_CONFIG
                               )

Player = namedtuple("Player", ["name", "score", "kills", "deaths",
                               "plants", "defuses", "map",
                               "top_fragger", "zero_bomb"])
Word = namedtuple("Word", ["text", "x", "y"])


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


def parse_response(response):
    words = get_words(response)

    rows = group_words_into_rows(words)

    game_map = get_game_map_from_rows(rows)

    away_players, home_players = get_players(game_map, rows)

    home_players = assign_top_fragger(home_players)
    away_players = assign_top_fragger(away_players)

    home_players = assign_zero_bomb(home_players)
    away_players = assign_zero_bomb(away_players)

    return pd.DataFrame(data=home_players+away_players)


def get_players(game_map, rows):
    home_players = []
    away_players = []
    for row in reversed(rows):
        row = mwrvr.misc.convert_common_ocr_errors(row)

        # go backwards through the rows until we get to table headers
        if is_table_header(row):
            break

        if len(row) == 12:
            home_player, away_player = process_players(row, game_map)

            if home_player is not None:
                home_players.append(home_player)

            if away_player is not None:
                away_players.append(away_player)
    return away_players, home_players


def get_words(response, decimal_places=1):
    words = []
    for block in response["Blocks"]:
        if block["BlockType"] == "WORD":
            words.append(get_word(block, decimal_places))
    return words


def process_players(row, game_map):
    try:
        home_player_name = row[0]
        home_player_stats = [int(x) for x in row[1:6]]
        home_player = Player(home_player_name, *home_player_stats, map=game_map,
                             top_fragger=0, zero_bomb=0)
    except ValueError:  # some values in the stats can't be converted to an int
        home_player = None
    try:
        away_player_name = row[6]
        away_player_stats = [int(x) for x in row[7:]]
        away_player = Player(away_player_name, *away_player_stats, map=game_map,
                             top_fragger=0, zero_bomb=0)
    except ValueError:  # some values in the stats can't be converted to an int
        away_player = None

    return home_player, away_player


def get_word(block, decimal_places=1):
    """Get a word from a block and return a Word namedtuple."""
    return (
        Word(block.get("Text"),
             np.round(get_left_of_word(block), decimal_places),
             np.round(get_middle_of_word(block), decimal_places))
    )


def get_left_of_word(block):
    return block.get("Geometry").get("BoundingBox").get("Left")


def get_middle_of_word(block):
    return (
            (2 * block.get("Geometry").get("BoundingBox").get("Top")
             + block.get("Geometry").get("BoundingBox").get("Height")
             ) / 2
    )


def group_words_into_rows(words):
    rows = groupby(words, key=lambda x: x.y)
    rows = [[item[0] for item in data] for (key, data) in rows]
    return rows


def get_game_map_from_rows(rows):
    game_map = None
    for row in rows:
        for word in row:
            if word.upper() in mwrvr.constants.MWR_MAPS:
                game_map = word
                break
    if game_map is None:
        game_map = "UNKNOWN"

    return game_map


def assign_top_fragger(players: list):
    try:
        sorted_players = list(sorted(players, key=lambda x: int(x.kills), reverse=True))
        sorted_players[0] = sorted_players[0]._replace(top_fragger=1)
        for i, player in enumerate(sorted_players):
            if int(player.kills) == int(sorted_players[0].kills):
                sorted_players[i] = player._replace(top_fragger=1)
        return sorted_players
    except Exception:
        # TODO - sometimes players is an empty list
        return players


def assign_zero_bomb(players: list):
    new_players = []
    for player in players:
        if player.kills == 0:
            new_players.append(player._replace(zero_bomb=1))
        else:
            new_players.append(player)
    return new_players


def is_table_header(row):
    if "PLAYER" in row and "SCORE" in row:
        return True
    return False
