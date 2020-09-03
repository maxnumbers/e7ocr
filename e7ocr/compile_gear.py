from glob import glob
from string import ascii_lowercase, digits
import random
import json
import cv2


def export_gear_to_json(file_paths, corners=dict):
    print("Beginning export process...")

    for n, file_name in enumerate(file_paths):

        temp_list = []
        img = cv2.imread(file_name)
        print("currently processing: ", file_name)

        for key, coord in category_coords.items:
            ""

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

