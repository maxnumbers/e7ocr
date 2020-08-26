import pytesseract

# COMMENT IF NOT USING WINDOWS (i.e., add # before both lines)
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"

# Change to False if you always want your actual main stat value
assume_max_lv_gear = True

# Screenshot path
sh_path = "screenshots/"

from PIL import Image
from pytesseract import image_to_string


def process(k, img):
    if k == "plus" or k == "level":
        # Since level and plus are read off the gear icon, there is a lot of noise
        # So we need an iterative process to try to extract a value
        thresh = cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        low = 81
        proc = cv2.cvtColor(
            cv2.medianBlur(
                cv2.threshold(
                    cv2.cvtColor(
                        cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_RGB2GRAY
                    ),
                    low,
                    255,
                    thresh,
                )[1],
                3,
            ),
            cv2.COLOR_GRAY2RGB,
        )
        data = (
            image_to_string(Image.fromarray(proc), lang="eng", config="--psm 7")
            .replace("+b", "6")
            .replace(">", "0")
        )
        if not any(i.isdigit() for i in data):
            low = 100
            proc = cv2.cvtColor(
                cv2.medianBlur(
                    cv2.threshold(
                        cv2.cvtColor(
                            cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_RGB2GRAY
                        ),
                        low,
                        255,
                        thresh,
                    )[1],
                    3,
                ),
                cv2.COLOR_GRAY2RGB,
            )
            data = (
                image_to_string(Image.fromarray(proc), lang="eng", config="--psm 7")
                .replace("+b", "6")
                .replace(">", "0")
            )
            if not any(i.isdigit() for i in data):
                low = 125
                proc = cv2.cvtColor(
                    cv2.medianBlur(
                        cv2.threshold(
                            cv2.cvtColor(
                                cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_RGB2GRAY
                            ),
                            low,
                            255,
                            thresh,
                        )[1],
                        3,
                    ),
                    cv2.COLOR_GRAY2RGB,
                )
                data = (
                    image_to_string(Image.fromarray(proc), lang="eng", config="--psm 7")
                    .replace("+b", "6")
                    .replace(">", "0")
                )
                if not any(i.isdigit() for i in data):
                    data = str(0)

    else:
        thresh = cv2.THRESH_BINARY_INV
        low = 70
        proc = cv2.cvtColor(
            cv2.medianBlur(
                cv2.threshold(
                    cv2.cvtColor(
                        cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY
                    ),
                    low,
                    255,
                    thresh,
                )[1],
                3,
            ),
            cv2.COLOR_GRAY2RGB,
        )
        data = (
            image_to_string(Image.fromarray(proc), lang="eng", config="--psm 6")
            .replace("Rina", "Ring")
            .replace("Edic", "Epic")
            .replace("Enic", "Epic")
        )
    return data


def stat_converter(stat):
    result = ""
    if "attack" in stat.lower():
        result = "Atk"
        if "%" in stat:
            result += "P"
    if "health" in stat.lower():
        result = "HP"
        if "%" in stat:
            result += "P"
    if "defense" in stat.lower():
        result = "Def"
        if "%" in stat:
            result += "P"
    if "speed" in stat.lower():
        result = "Spd"
    if "chance" in stat.lower():
        result = "CChance"
    if "damage" in stat.lower():
        result = "CDmg"
    if "effectiveness" in stat.lower():
        result = "Eff"
    if "resistance" in stat.lower():
        result = "Res"
    return result


def digit_filter(val):
    if not val:
        return 0
    elif val == ".":
        return 0
    else:
        return int("".join(filter(str.isdigit, val)))


def char_filter(val):
    return "".join(filter(str.isalpha, val)).capitalize()


def max_stat(data, item):
    stat = stat_converter(data)
    val = digit_filter(data)  # Begin by setting val = actual value
    if (
        item["ability"] < 15
    ):  # Only change stats on items where they need to be increased
        if item["level"] in range(58, 73):
            if stat == "CChance":
                val = 45
            elif stat == "CDmg":
                val = 55
            elif stat == "Spd":
                val = 35
            elif item["slot"] == ("Necklace" or "Ring" or "Boots"):
                val = 50
            elif stat == "HP":
                val = 2295  # Not exactly right, finer-grained scaling
            elif stat == "Def":
                val = 250  # Not exactly right, finer-grained scaling
            elif stat == "Atk":
                val = 425  # Not exactly right, finer-grained scaling
        elif item["level"] in range(74, 86):
            if stat == "CChance":
                val = 55
            elif stat == "CDmg":
                val = 65
            elif stat == "Spd":
                val = 40
            elif item["slot"] == ("Necklace" or "Ring" or "Boots"):
                val = 60
            elif stat == "HP":
                val = 2700  # Not exactly right, finer-grained scaling
            elif stat == "Def":
                val = 300  # Not exactly right, finer-grained scaling
            elif stat == "Atk":
                val = 500  # Not exactly right, finer-grained scaling
        elif item["level"] in range(87, 89):
            if stat == "CChance":
                val = 60
            elif stat == "CDmg":
                val = 70
            elif stat == "Spd":
                val = 45
            elif item["slot"] == ("Necklace" or "Ring" or "Boots"):
                val = 65
            elif stat == "HP":
                val = 2765
            elif stat == "Def":
                val = 310
            elif stat == "Atk":
                val = 515
    return val
