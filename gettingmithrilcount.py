import mss
import numpy as np
import cv2
from paddleocr import PaddleOCR
import time
import re
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
time.sleep(5)

# Initialize mss
sct = mss.mss()
time.sleep(2)
# Define the region for the text

text_region = {"top": 450, "left": 1650, "width": 250, "height": 100,"monitor": sct.monitors[1]}
screenshot = np.array(sct.grab(text_region))
# Capture the screen region
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)
# Convert to grayscale for OCR
result = ocr.ocr(screenshot, cls=True)
print (result)
mithrilcheck = ""
if result[0] == None:
    print("It is none :(")
else:
    for i in range(len(result[0])):
        if "Mithril" in result[0][i][1][0]:
            mithrilcheck = re.sub(r"\D", "", result[0][i][1][0])
            break
mithrilcount = int(mithrilcheck)
print(mithrilcount)
