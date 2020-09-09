from glob import glob
from string import ascii_lowercase, digits
import random
import json
import cv2
import pytesseract

#### Uncomment These If Using WINDOWS ####
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"

export = {"processVersion": "1", "heroes": [], "items": []}

OCR_filter = {
    "level_range": {
        0: range(16),
        1: range(16, 30),
        2: range(30, 44),
        3: range(44, 58),
        4: range(58, 72),
        5: range(72, 86),
        6: range(86, 98),
    },
    "main_stat": {
        "CChance": [5, 15, 25, 35, 45, 55, 60],
        "CDmg": [15, 25, 35, 45, 55, 65, 70],
        "Spd": [15, 20, 25, 30, 35, 40, 45],
        "HP": [None, None, None, 1760, 2360, 2700, 2765],
        "Def": [None, None, None, 190, 260, 300, 310],
        "Atk": [None, None, None, 330, 440, 500, 510],
    },
    "expected_text": {
        "stat_type": [
            "Attack",
            "Defense",
            "Health",
            "Speed",
            "Critical Hit Chance",
            "Critical Hit Damage",
            "Effectiveness",
            "Effect Resist",
            "Dual Attack Chance",
        ],
        "level": list(range(91)),
        "plus": list(range(1, 16)),
        "rarity": [
            "Normal",
            "Good",
            "Rare",
            "Heroic",
            "Epic"],
        "slot": [
            "Weapon",
            "Helmet",
            "Armor",
            "Necklace",
            "Ring",
            "Boots"],
        "sets": [
            "Attack",
            "Health",
            "Defense",
            "Unity",
            "Counter",
            "Resist",
            "Lifesteal",
            "Immunity",
            "Hit",
            "Critical",
            "Speed",
            "Destruction",
            ],
    },
}

# TODO  reference API for langs @ https://github.com/EpicSevenDB/ui/blob/master/lang/de-DE.js


def E7_OCR(screenshots_path, auto_max_main=True, ):
    print("ffs")

def max_stat(data,item):
    stat = stat_converter(data)
    val = digit_filter(data) # Begin by setting val = actual value
    if item['ability'] < 15: # Only change stats on items where they need to be 


    # A common OCR error is to fail to read the level. If this happens, we need to set it to 1 so it will import properly.
    if item['level'] == 0:
        item['level'] = 1
    #print(item)
    
    #checks to see if there are duplicates, and if not, give item unique ID and place in 'export'
    if item not in temp_list:
        temp_list.append(item)
        #print(export['items'])
        item['id'] = 'jt'+''.join(random.choice(digits+ascii_lowercase) for _ in range(6))
        export['items'].append(item)
    
    # outputs progress of export
    print(len(export['items']),"exported out of",len(filenames))
    return


    print(name, "shows lvl", item['level'],"and enhance lv",item['ability'])
#export to json for importing into optimizer
with open('exported_gear.json', 'w') as f: json.dump(export, f)
print('JSON file finished!')