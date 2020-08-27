from PIL import Image
from pytesseract import Output
from pprint import pprint
from matplotlib import pyplot as plt
import pytesseract
import glob
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"
filename = "2.png"
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

# # for testing; prints window w/ edges being grabbed
# cv2.imshow("Image", edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

equip_display_borders = cv2.HoughLinesP(
    edges, 1, np.pi / 180, 100, minLineLength, maxLineGap
)
no_of_lines_found = len(equip_display_borders)
# print(no_of_lines_found, " lines were found as borders")

# check that at least 4, but less than 8 boundary lines found

for line in equip_display_borders:
    for x1, y1, x2, y2 in line:
        if (no_of_lines_found > 4):
            for x1_vals in enumerate()
    
        # line is good :D
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

