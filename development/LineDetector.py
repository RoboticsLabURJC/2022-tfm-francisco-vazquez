import math
import cv2
import numpy as np


class LineDetector:
    _width = None
    _heidth = None

    def __int__(self):
        self._width = 640
        self._heidth = 480

    def detect_points(self, image):
        edges_canny = cv2.Canny(image, threshold1=50, threshold2=120)
        # cv2.imshow("canny", edges_canny)

        kernel = np.ones((5, 5), np.uint8)
        edges_dilated = cv2.dilate(edges_canny, kernel, iterations=3)
        edges_eroded = cv2.erode(edges_dilated, kernel, iterations=3)
        # cv2.imshow("erpo", edges_eroded)
        x1, y1 = None, None
        x2, y2 = None, None

        for x in range(325, 640):
            if edges_eroded[310, x] == 255:
                x1, y1 = x, 310
                break

        for x in range(315, 0, -1):
            if edges_eroded[310, x] == 255:
                x2, y2 = x, 310
                break

        return x1, y1, x2, y2



