import mss
import numpy as np
import time
def get_pixel_color(x, y, region):
    with mss.mss() as sct:
        # Capture the screen region
        screenshot = np.array(sct.grab(region))

    # Get the pixel color at (x, y)
    color = screenshot[y, x, :3]  # Extract RGB values (ignore alpha channel)
    return color
while True:
    sct = mss.mss()

    colr = get_pixel_color(244, 244, {"top": 296, "left": 716, "width": 488, "height": 488, "monitor" : sct.monitors[1]})
    print(colr)
    print("R: ",colr[0])
    print("G: ",colr[1])
    print("B: ",colr[2])
    time.sleep(0.5)


    #mss does capture in bgr format, so we need to convert it to rgb format