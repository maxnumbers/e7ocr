from glob import glob
from string import ascii_lowercase, digits
import random
import json
import cv2
import pytesseract


CDmg_range = list(range(15, 66, 10))  # needs 70 as final value

# TODO instead of manually inputting text, use links to E7 API because it has the other language translations


export = {"processVersion": "1", "heroes": [], "items": []}
OCR_filter = {
    "range": {
        0: range(16),
        1: range(16, 30),
        2: range(30, 44),
        3: range(44, 58),
        4: range(58, 72),
        5: range(72, 86),
        6: range(86, 98),
    },
    "main_stat": {
        "CChance": list(range(5, 66, 5)),
        "CDmg": list(range(15, 66, 10), 70),
        "Spd": list(range(15, 5, 46)),
        "HP": [None, None, None, 1760, 2360, 2700, 2765],
        "Def": [None, None, None, 190, 260, 300, 310],
        "Atk": [None, None, None, 330, 440, 500, 510],
    },
    "text": {
        "stat_types": [],
        "levels": [],
        "plus": [],
        "rarity": [],
        "slot": [],
        "ability": [],
        "main": [],
        "subs": [],
        "set": [],
    },
}


def E7_OCR(screenshots_path, assume_max_main_stat=True):

    return
