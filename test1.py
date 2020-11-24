import cv2
import numpy as np
import math
from clefFind import *

img = cv2.imread('Tm1.png')

imgGr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
image_width = img.shape[1]
image_height = img.shape[0]

_,imgGr = cv2.threshold(imgGr,200,255,cv2.THRESH_BINARY_INV)

MIN_HOUGH_VOTES_FRACTION = 0.05  # Minimum points on a line (as fraction of image width)
MIN_LINE_LENGTH_FRACTION = 0.06  # Minimum length of a line (as a fraction of image width)
# Run Hough transform.  The output hough_lines has size (N,1,2), where N is #lines.
# The 3rd dimension has values rho,theta for the line.
hough_lines = cv2.HoughLinesP(
    image=imgGr,
    rho=1,  # Distance resolution of the accumulator in pixels
    theta=math.pi / 180,  # Angle resolution of the accumulator in radians
    threshold=int(image_width * MIN_HOUGH_VOTES_FRACTION),  # Accumulator threshold (get lines where votes>threshold)
    lines=None,
    minLineLength=int(image_width * MIN_LINE_LENGTH_FRACTION),
    maxLineGap=10)
print("Number of lines: %d" % len(hough_lines))

key = clefFind(imgGr)

print(key)
lineOut = imgGr
for i in range(len(hough_lines)):
    l = hough_lines[i][0]
    cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0, 0, 255),
             thickness=2, lineType=cv2.LINE_AA)
    cv2.line(lineOut, (l[0], l[1]), (l[2], l[3]), (0, 0, 0),
             thickness=1, lineType=cv2.LINE_AA)


cv2.imshow('lines',img)
cv2.waitKey()

cv2.imshow('no line',lineOut)
cv2.waitKey()

ksize = 4
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_CLOSE,kernel)
#lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_OPEN,kernel)

cv2.imshow('morphed',lineOut)
cv2.waitKey()