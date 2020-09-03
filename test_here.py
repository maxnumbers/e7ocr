import pytesseract
import glob
import numpy as np
from e7ocr.img_processing import box_boundaries

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"


# file paths
filename = "test_2.jpg"
filenames = glob(sh_path + "*.png")
filenames.extend(glob(sh_path + "*.jpg"))

# preprocess image
corners = box_boundaries(filename)

# send/recieve w/ tesseract to output JSON

