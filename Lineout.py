import cv2
import numpy as np
import math

def lineout(img):
    image_width = img.shape[1]
    image_height = img.shape[0]
    MIN_HOUGH_VOTES_FRACTION = 0.05  # Minimum points on a line (as fraction of image width)
    MIN_LINE_LENGTH_FRACTION = 0.06  # Minimum length of a line (as a fraction of image width)
    # Run Hough transform.  The output hough_lines has size (N,1,2), where N is #lines.
    # The 3rd dimension has values rho,theta for the line.
    hough_lines = cv2.HoughLinesP(
        image=img,
        rho=2,  # Distance resolution of the accumulator in pixels
        theta=math.pi / 180,  # Angle resolution of the accumulator in radians
        threshold=int(image_width * MIN_HOUGH_VOTES_FRACTION),
        # Accumulator threshold (get lines where votes>threshold)
        lines=None,
        minLineLength=int(image_width * MIN_LINE_LENGTH_FRACTION),
        maxLineGap=10)
    lineOut = img
    lineHeight = []
    for i in range(len(hough_lines)):
        l = hough_lines[i][0]
        cv2.line(lineOut, (l[0], l[1]), (l[2], l[3]), (0, 0, 0),
                 thickness=1, lineType=cv2.LINE_AA)
        lineHeight.append(l[3])

    for height in lineHeight:
        d = [H - height for H in lineHeight]
        for dist in d:
            if dist == 0:
                continue
            elif abs(dist) < 3:
                lineHeight.remove(height)
    lineHeight.sort()
    return [lineOut,lineHeight]