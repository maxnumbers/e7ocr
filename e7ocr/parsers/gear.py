from glob import glob
from string import ascii_lowercase, digits
import random
import json
import cv2

# initialize all vars
export = {"processVersion": "1", "heroes": [], "items": []}
temp_list = []
filenames = glob(sh_path + "*.png")
filenames.extend(glob(sh_path + "*.jpg"))


def export_gear_to_json():
    print("Beginning export process...")

    for n, name in enumerate(filenames):

        # The height of the item box changes depending on the length of the item and set descriptions,
        # we have to crop the top and bottom info separately in order to ensure the OCR boxes within these areas
        # remain in fixed locations. we then process the top and bottom info independently.

        img = cv2.imread(name)

        # Top box
        temp_top = cv2.imread("e7/top.jpg", 0)
        a, b, c, max_loc = cv2.minMaxLoc(
            cv2.matchTemplate(
                cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_top, cv2.TM_CCOEFF_NORMED
            )
        )
        top_box = img[
            max_loc[1] : max_loc[1] + 160, 740:1190
        ]  # Fixed width, then crop 160 pixels from top triangle

        # Bottom box
        temp_bot = cv2.imread("e7/bottom.jpg", 0)
        a, b, c, max_loc = cv2.minMaxLoc(
            cv2.matchTemplate(
                cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_bot, cv2.TM_CCOEFF_NORMED
            )
        )
        bottom_box = img[
            max_loc[1] + 25 : max_loc[1] + 360, 740:1190
        ]  # Fixed width, shift down 25 from divider, then crop 335 pixels deep

        # Setup item dictionary
        item = {"locked": False, "efficiency": 0}

        # Process top image
        top_coords = {
            "type": [[20, 70], [172, 432]],
            "level": [[19, 44], [37, 66]],
            "plus": [[11, 34], [139, 168]],
        }

        print("currently processing", name)

        for k in top_coords.keys():
            data = process(
                k,
                top_box[
                    top_coords[k][0][0] : top_coords[k][0][1],
                    top_coords[k][1][0] : top_coords[k][1][1],
                ],
            )
            if k == "type":
                item["rarity"] = char_filter(data.split(" ")[0])
                item["slot"] = char_filter(data.split(" ")[1].split("\n")[0])
            if k == "level":
                item["level"] = digit_filter(
                    data.replace("S", "5").replace("B", "8").replace("a", "8")
                )
            if k == "plus":
                item["ability"] = digit_filter(
                    data.replace("S", "5").replace("B", "8").replace("a", "8")
                )

        print(name, "shows lvl", item["level"], "and enhance lv", item["ability"])

        # Process bottom image
        bot_coords = {
            "main": [[8, 70], [65, 435]],
            "subs": [[98, 255], [25, 435]],
            "set": [[280, 340], [76, 435]],
        }

        for k in bot_coords.keys():
            data = process(
                k,
                bottom_box[
                    bot_coords[k][0][0] : bot_coords[k][0][1],
                    bot_coords[k][1][0] : bot_coords[k][1][1],
                ],
            )
            if k == "main":
                stat = stat_converter(data)
                if assume_max_lv_gear is True:
                    item["mainStat"] = [stat, max_stat(data, item)]
                else:
                    item["mainStat"] = [stat, digit_filter(data)]

            if k == "subs":
                for n, entry in enumerate(data.split("\n")):
                    stat = stat_converter(entry)
                    val = digit_filter(entry.replace("T", "7"))
                    item["subStat" + str(n + 1)] = [stat, val]
            if k == "set":
                item["set"] = char_filter(data.split(" Set")[0])

        # A common OCR error is to fail to read the level. If this happens, we need to set it to 1 so it will import properly.
        if item["level"] == 0:
            item["level"] = 1

        # Check to see if there are duplicates, and if not, give item unique ID and place in 'export'
        if item not in temp_list:
            temp_list.append(item)
            item["id"] = "jt" + "".join(
                random.choice(digits + ascii_lowercase) for _ in range(6)
            )
            export["items"].append(item)

        print(len(export["items"]), "exported out of", len(filenames))

    # Export dictionary to json for importing into optimizer
    with open("exported_gear.json", "w") as f:
        json.dump(export, f)

    print("JSON file finished!")

