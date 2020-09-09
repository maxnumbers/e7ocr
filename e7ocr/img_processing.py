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

class setup:
    """ class object with the following attributes:
    - self.img          : image 
    - self.shape        : tuple(int,int)
    - self.filename     : string
    - self.print_lines  : tuple(int,int,int,int)
    - self.bounds       : dict
    - self.bounds_img   : image
    - self.sections     : dict of coords
    """

    def __init__(self, filename, print_lines=False):
        self.print_lines = print_lines
        self.cropped_imgs = []
        self.filename = filename
        self.image = cv2.imread(self.filename)
        self.perimeter_lines = determine_perimeter_lines(self)
        self.perimeter_line_count = len(self.perimeter_lines)

        # check that at least 4, but less than 8 boundary lines found
        while self.perimeter_line_count > 4:
            remove_perimeter_duplicates(self)

        self.bounds = determine_template_bounds(self)
        self.sections = crop_n_section_img(self)

def _display_image(image):
    
    x_dim,y_dim,channel = image.shape
    if x_dim > 1900 or y_dim > 1000:
        dims = (1900,1000)
        image = cv2.resize(image, dims)
        

    cv2.imshow("Image Pre-view", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

def _if_print_lines(self, func_img):
    if self.print_lines is True:
        _display_image(func_img)

# TODO Add change crop_n_section so that cropping is a function
# def _crop_image_and_display(self, x_percent, y_percent, crop_index, start_at_top):
#     self.cropped_imgs.append(self.cropped_imgs[crop_index][:, :])
    
#     _if_print_lines(self, self.cropped_imgs[-1])
    

def determine_perimeter_lines(self):

    color_img = cv2.imread(self.filename)
    img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    # increasing aperture = more detail (which is bad here)
    edges = cv2.Canny(img, 90, 150, apertureSize=3)
    dims = img.shape
    self.shape = img.shape

    # evaluate images by relative locations
    minLineLength = min(dims[:1]) // 2
    maxLineGap = minLineLength // 1.05
    equip_display_border_coords = np.reshape(
        cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap),
        (-1, 4),
    )
    # TODO change all reshapes because they seem to change the order of the coords
    # test with test_3.jpg

    if self.print_lines is True:
        # creates lines on image where there are lines
        for x1, y1, x2, y2 in equip_display_border_coords:
            lined_img = cv2.line(color_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        _display_image(lined_img)

    return equip_display_border_coords

def remove_perimeter_duplicates(self):

    # compares line coord sets: [(x,y,x,y),(x,y,x,y)]
    comparison_combos = combinations(self.perimeter_lines, 2)

    for line_1_coords, line_2_coords in comparison_combos:

        line_location_diff = abs(line_1_coords - line_2_coords)

        count_less_than_4 = 0
        for coord in line_location_diff:
            if coord < 4:
                count_less_than_4 = count_less_than_4 + 1

        if count_less_than_4 > 2:

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
                self.perimeter_lines = self.perimeter_lines[
                    self.perimeter_lines != line_2_coords
                ].reshape(-1, 4)

            else:
                self.perimeter_lines = self.perimeter_lines[
                    self.perimeter_lines != line_1_coords
                ].reshape(-1, 4)

            self.perimeter_line_count = len(self.perimeter_lines)
            break

def determine_template_bounds(self):
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

    self.top = up
    self.bot = down
    self.left = left
    self.right = right

def crop_n_section_img(self):

    bounds_img = self.image

    # crop to equip box (eb): 
    equip_box = bounds_img[
        self.top : self.bot,
        self.left : self.right,
        ]

    # crop 35% off right side of equip box
    eb_x = round(.65*(self.right - self.left))
    eb_y = (self.bot - self.top)
    _if_print_lines(self, equip_box)

    # top 1/2 of equip box (teb)0
    top_equip_box = equip_box[0:round(.53*eb_y), 0:eb_x]
    _if_print_lines(self, top_equip_box)

    # bottom 1/2 of equip box (beb)
    bot_equip_box = equip_box[round(.53*eb_y):eb_y, 0:eb_x]
    _if_print_lines(self, bot_equip_box)

    category_coords = {
        "type": [[], []],
        "level": [[], []],
        "plus": [[], []],
        "main": [[], []],
        "subs": [[], []],
        "set": [[], []],
    }

    return category_coords

