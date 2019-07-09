from loguru import logger

import mwrvr.ocr
import mwrvr.constants


def get_team_result_status(image, players_per_team, left_team=True):
    """Return the portion of the image that contains the status of the home team."""
    assert players_per_team in mwrvr.constants.ALLOWED_TEAM_SIZES, ("Can only find "
                       f"scoreboards which have {mwrvr.constants.ALLOWED_TEAM_SIZES} "
                                                                    "players per team")

    if left_team:
        scoreboard_bbox = (
            mwrvr.constants.SCOREBOARD_LEFT_TEAM_RESULT_BOUNDING_BOXES[players_per_team]
        )
    else:
        scoreboard_bbox = (
            mwrvr.constants.SCOREBOARD_RIGHT_TEAM_RESULT_BOUNDING_BOXES[
                players_per_team]
        )

    return mwrvr.ocr.ocr_string(
        image[
            scoreboard_bbox[0]:
            scoreboard_bbox[1],
            scoreboard_bbox[2]:
            scoreboard_bbox[3]
        ]
    )


def victory_or_defeat_in_results(results):
    return (any("VICTORY" in result for result in results) or
            any("DEFEAT" in result for result in results))


def is_final_scoreboard(image):
    """Given an image, return whether or not the image is an MWR final scoreboard."""
    left_results = [get_team_result_status(image, i, left_team=True)
                    for i in mwrvr.constants.ALLOWED_TEAM_SIZES]

    if victory_or_defeat_in_results(left_results):

        right_results = [get_team_result_status(image, i, left_team=False)
                         for i in mwrvr.constants.ALLOWED_TEAM_SIZES]

        if victory_or_defeat_in_results(right_results):
            return True

    return False


def crop_scoreboard(image):
    return image[
               mwrvr.constants.SCOREBOARD_BOUNDING_BOX[0]:
               mwrvr.constants.SCOREBOARD_BOUNDING_BOX[1],
               mwrvr.constants.SCOREBOARD_BOUNDING_BOX[2]:
               mwrvr.constants.SCOREBOARD_BOUNDING_BOX[3]
           ]
