import mss
import cv2
import numpy as np


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        img = np.array(screenshot)

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        filename = "screen.jpg"

        cv2.imwrite(filename, img)

        return filename