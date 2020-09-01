import pytesseract
import glob
import numpy as np
from e7ocr.transmuters.tesseract import get_equip_location

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"
filename = "test_2.jpg"
line_coords = ""

corners = get_equip_location(filename)
print(corners)
