import mss
import numpy as np
import cv2
from paddleocr import PaddleOCR
import time
import re

time.sleep(5)
sct = mss.mss()
time.sleep(2)
screen_region = {"top": 174, "left": 594, "width": 732, "height": 732, "monitor" : sct.monitors[1]}
screenshot = np.array(sct.grab(screen_region))

cv2.imshow("image",screenshot)
cv2.waitKey(10000)