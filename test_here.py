from PIL import Image
from pytesseract import Output
from pprint import pprint
from matplotlib import pyplot as plt
from itertools import combinations
import pytesseract
import glob
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"
filename = "test_2.jpg"
line_coords = ""

# def _determine_equip_display_dims(filename):
img = cv2.imread(filename)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# increasing aperture = more detail (which is bad here)
edges = cv2.Canny(gray_img, 90, 150, apertureSize=3)
image_xy = img.shape[:1]

# evaluate images by relative locations
minLineLength = min(image_xy) // 2
maxLineGap = minLineLength // 1.025

""" # for testing; prints window w/ edges being grabbed
cv2.imshow("Image", edges)
cv2.waitKey(0)
cv2.destroyAllWindows() """

equip_display_borders = cv2.HoughLinesP(
    edges, 1, np.pi / 180, 100, minLineLength, maxLineGap
)
compare_lines_arr = np.array(equip_display_borders)
no_of_lines_found = len(equip_display_borders)
# print(no_of_lines_found, " lines were found as borders")

# check that at least 4, but less than 8 boundary lines found
while no_of_lines_found > 4:

    # compares line coord sets: [(x,y,x,y),(x,y,x,y)]
    comparison_combos = combinations(equip_display_borders, 2)

    for combo in comparison_combos:
        line_1_coords = combo[0]
        line_2_coords = combo[1]

        # check location has 4 values (x,y,x,y)
        line_location_diff = line_1_coords - line_2_coords
        if any in abs(line_location_diff[0]) < 4:

            # take longer line if same line length should be a function; t
            line_1_length = (
                (abs(line_1_coords[0][0] - line_1_coords[0][2]) ** 2)
                + (abs(line_1_coords[0][1] - line_1_coords[0][3]) ** 2)
            ) ** 0.5
            line_2_length = (
                (abs(line_2_coords[0][0] - line_2_coords[0][2]) ** 2)
                + (abs(line_2_coords[0][1] - line_2_coords[0][3]) ** 2)
            ) ** 0.5

            if line_1_length > line_2_length:
                equip_display_borders.remove([line_2_coords])

            else:
                equip_display_borders.remove([line_1_coords])

            no_of_lines_found = len(equip_display_borders)

    # TODO want to add check for x1,y1 values being to close to other line's values
    # if w/in ~5-10 pixels of one another
    # delete the shorter line

for line in equip_display_borders:
    for x1, y1, x2, y2 in line:
        "placeholder"
        # creates a line on the image so that you can see where it beleives the line is
        # cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # interpret the box borders
    #  value we care about's x1 = x2 or y1 = y2... only one will be true
    equip_box_corners: {
        "top_left": (x_same_small, y_same_small),
        "top_right": (x_same_large, y_same_small),
        "bottom_left": (x_same_small, y_same_large),
        "bottom_right": (x_same_large, y_same_large),
    }
    # return equip_box_corners

# cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
# cv2.imshow("Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

