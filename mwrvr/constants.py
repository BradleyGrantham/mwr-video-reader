SCOREBOARD_LEFT_TEAM_RESULT_BOUNDING_BOXES = {
    2: [316, 356, 215, 350],
    3: [308, 348, 215, 350],
    4: [300, 340, 215, 350],
    5: [292, 332, 215, 350]
}

SCOREBOARD_RIGHT_TEAM_RESULT_BOUNDING_BOXES = {
    2: [316, 356, -360, -225],
    3: [308, 348, -360, -225],
    4: [300, 340, -360, -225],
    5: [292, 332, -360, -225]
}

assert (
        set(SCOREBOARD_RIGHT_TEAM_RESULT_BOUNDING_BOXES.keys())
        == set(SCOREBOARD_LEFT_TEAM_RESULT_BOUNDING_BOXES.keys())
)
ALLOWED_TEAM_SIZES = set(SCOREBOARD_RIGHT_TEAM_RESULT_BOUNDING_BOXES.keys())

SCOREBOARD_BOUNDING_BOX = [250, -250, 120, -120]

FPS = 30

TESSERACT_CONFIG = "--psm 13"


MWR_MAPS = ["AMBUSH",
            "BACKLOT",
            "BOG",
            "BLOC",
            "BROADCAST",
            "CHINATOWN",
            "CREEK",
            "KILLHOUSE",
            "COUNTDOWN",
            "CRASH",
            "CROSSFIRE",
            "DISTRICT",
            "DOWNPOUR",
            "OVERGROWN",
            "PIPELINE",
            "SHIPMENT",
            "SHOWDOWN",
            "STRIKE",
            "VACANT",
            "WETWORK",
            "WINTER CRASH",
            "BEACH BOG"
            ]

TEAM_MEMBERS = ["ntsfbrad", "Jordanx267", "LazyJakeyy", "bennettar95", "JaAnTr"]