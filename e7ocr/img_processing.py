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


class setup_image:
    def __init__(self, filename, print_lines=False):
        self.filename = filename
        self.print_lines = print_lines
        self.perimiter_lines = perimiter_lines(print_lines)
        self.perimeter_line_count = len(self.peremiter_lines)

        # check that at least 4, but less than 8 boundary lines found
        while self.border_line_count > 4:
            filter_perimeter()

        self.bounds = determine_bounds()
        self.OCR_crop_template = crop_n_section_img()

    def perimeter_lines(self):

        color_img = cv2.imread(self.filename)
        img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        # increasing aperture = more detail (which is bad here)
        edges = cv2.Canny(img, 90, 150, apertureSize=3)
        img_xy = img.shape[:1]

        # evaluate images by relative locations
        minLineLength = min(img_xy) // 2
        maxLineGap = minLineLength // 1.025

        equip_display_border_coords = np.reshape(
            cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap),
            (5, 4),
        )

        if print_lines is True:
            for x1, y1, x2, y2 in equip_display_border_coords:
                cv2.line(color_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # for testing; prints window w/ edges being grabbed
            cv2.imshow("Image", color_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return equip_display_border_coords

    def filter_perimeter(self):

        # compares line coord sets: [(x,y,x,y),(x,y,x,y)]
        comparison_combos = combinations(self.peremeter_lines, 2)

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
                    self.peremiter_lines = self.peremeter_lines[
                        self.peremeter_lines != line_2_coords
                    ].reshape(4, 4)

                else:
                    self.peremiter_lines = self.peremeter_lines[
                        self.peremeter_lines != line_1_coords
                    ].reshape(4, 4)

                self.perimeter_line_count = len(self.peremiter_lines)
                break

    def determine_bounds(self):
        x_coords = []
        y_coords = []

        for coord_set_index, coord_set in enumerate(self.perimeter_lines):
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

        (up, down) = np.sort(y_coords)
        (left, right) = np.sort(x_coords)

        bounds = {"up": up, "down": down, "left": left, "right": right}

        return bounds

    def crop_n_section_img(self):
        (y_top, y_bot, x_left, x_right) = (y_coords, x_coords)
        img = cv2.imread(filename)

        # crop to equip box
        cropped = img[y_top:y_bot, x_left:x_right]
        cropped_height = y_bot - y_top
        cropped_width = x_right - x_left

        # crop 35% off of right side
        ch0p = (0.35, 0.6)
        ch0 = ch0p[0] * cropped_height
        cw0_top = (1 - ch0p[1]) * cropped_width
        cw0_bot = (1 - (1 - ch0p[1])) * 0.4

        # top 20% of crop
        # bottom 20% of crop

        # middle 1/8 of crop

        category_coords = {
            "type": [[], []],
            "level": [[], []],
            "plus": [[], []],
            "main": [[], []],
            "subs": [[], []],
            "set": [[], []],
        }

        return category_coords

