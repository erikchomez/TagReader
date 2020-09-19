import cv2
import imutils
import numpy as np


def process_image(image_str: str) -> 'image':
    image = cv2.imread(image_str)
    image = imutils.resize(image, height=1000)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # edged = cv2.Canny(gray, 85, 45)
    edged = auto_canny(image)

    cv2.imwrite('edged_image.jpg', edged)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite('processed_image.jpg', image)


def auto_canny(image, sigma=0.3):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    return edged
