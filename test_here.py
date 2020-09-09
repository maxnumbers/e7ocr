import pytesseract
import glob
import numpy as np
from e7ocr.img_processing import setup

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"

# set file paths
filename = "test_1.jpg"
#filenames = glob(sh_path + "*.png")
#filenames.extend(glob(sh_path + "*.jpg"))

# process boundaries, returns: corners.
corners = setup(filename, print_lines = True)

# return boundary coords
# process boundary coords into sections
# 
# send/recieve w/ tesseract to output JSON

