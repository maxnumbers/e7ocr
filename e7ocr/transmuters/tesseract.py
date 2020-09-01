import pytesseract
import cv2
import numpy as np
from PIL import Image
from pytesseract import Output
from pprint import pprint
from matplotlib import pyplot as plt
from itertools import combinations

# COMMENT IF NOT USING WINDOWS (i.e., add # before both lines)
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"


def get_equip_location(filename, print=False):

    color_img = cv2.imread(filename)
    img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    # increasing aperture = more detail (which is bad here)
    edges = cv2.Canny(img, 90, 150, apertureSize=3)
    img_xy = img.shape[:1]

    # evaluate images by relative locations
    minLineLength = min(img_xy) // 2
    maxLineGap = minLineLength // 1.025

    equip_display_border_coords = np.reshape(
        cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap), (5, 4)
    )

    if print is True:
        for x1, y1, x2, y2 in equip_display_border_coords:
            cv2.line(color_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # for testing; prints window w/ edges being grabbed
        cv2.imshow("Image", color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    no_of_lines_found = len(equip_display_border_coords)
    box_coords = _get_equip_box_coords(equip_display_border_coords, no_of_lines_found)

    return box_coords


def _get_equip_box_coords(equip_coords_arr, no_of_lines_found):

    # check that at least 4, but less than 8 boundary lines found
    while no_of_lines_found > 4:

        # compares line coord sets: [(x,y,x,y),(x,y,x,y)]
        comparison_combos = combinations(equip_coords_arr, 2)

        for line_1_coords, line_2_coords in comparison_combos:

            line_location_diff = abs(line_1_coords - line_2_coords)

            if np.any(line_location_diff <= 2):

                # take longer line if same line length should be a function; t
                line_1_len = (
                    (abs(line_1_coords[0] - line_1_coords[2]) ** 2)
                    + (abs(line_1_coords[1] - line_1_coords[3]) ** 2)
                ) ** 0.5
                line_2_len = (
                    (abs(line_2_coords[0] - line_2_coords[2]) ** 2)
                    + (abs(line_2_coords[1] - line_2_coords[3]) ** 2)
                ) ** 0.5

                if line_1_len > line_2_len:
                    final_coords = equip_coords_arr[
                        equip_coords_arr != line_2_coords
                    ].reshape(4, 4)

                else:
                    final_coords = equip_coords_arr[
                        equip_coords_arr != line_1_coords
                    ].reshape(4, 4)

                no_of_lines_found = len(final_coords)
                break

    equip_corner_coords = _get_equip_corner_coords(final_coords)

    return equip_corner_coords


def _get_equip_corner_coords(final_coords):
    x_coords = []
    y_coords = []

    for coord_set_index, coord_set in enumerate(final_coords):
        (final_coord_values, final_coord_index, final_coord_count) = np.unique(
            coord_set, return_index=True, return_counts=True
        )

        for coord_index, unique_val in enumerate(final_coord_values):

            if final_coord_count[coord_index] > 1:
                # if coord has duplicates

                if final_coord_index[coord_index] in [0, 2]:
                    # remember: x1, y1, x2, y2
                    x_coords.append(unique_val)
                else:
                    y_coords.append(unique_val)

                break

    (y_top, y_bot) = np.sort(y_coords)
    (x_left, x_right) = np.sort(x_coords)

    equip_box_corners = {
        "top_left": (x_left, y_top),
        "top_right": (x_right, y_top),
        "bottom_left": (x_left, y_bot),
        "bottom_right": (x_right, y_bot),
    }

    return equip_box_corners

