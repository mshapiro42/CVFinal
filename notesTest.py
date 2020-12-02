import cv2
import numpy as np
import math
from clefFind import *

eighth1 = cv2.imread("eighth.jpg")
eighth2 = cv2.imread("eighth2.jpg")
quarter = cv2.imread("quarter.jpg")
half = cv2.imread("half.jpg")
notes = [eighth1,eighth2,quarter,half]
duration = np.array([.125,.125,.25,.5])
colors = [(255,0,255),(255,0,0),(0,255,0),(0,255,255)]
for n in range(len(notes)):
    tempT = notes[n]
    tempT = cv2.cvtColor(tempT, cv2.COLOR_BGR2GRAY)
    _, tempT = cv2.threshold(tempT, 200, 255, cv2.THRESH_BINARY)
    notes[n] = tempT

def findBestMatch(note):
    cv2.imshow("Note",note)
    cv2.waitKey(30)
    best = -1
    max = .3
    for i in range(len(notes)):
        noteFind = cv2.matchTemplate(note, notes[i], cv2.TM_CCOEFF_NORMED)
        hitN = np.amax(noteFind)
        if hitN>max:
            max = hitN
            best = i
    if best==-1:
        return 0
    elif (best==0 or best==1):
        return 1
    else:
        return best

def notesTest():
    img = cv2.imread('mySimpleSong3.jpg')

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
    lineLocs = []
    for i in range(len(hough_lines)):
        l = hough_lines[i][0]
        cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0, 0, 255),
                 thickness=1, lineType=cv2.LINE_AA)
        cv2.line(lineOut, (l[0], l[1]), (l[2], l[3]), (0, 0, 0),
                 thickness=1, lineType=cv2.LINE_AA)
        lineLocs.append(l[1])


    # cv2.imshow('lines',img)
    # cv2.waitKey()
    #
    # cv2.imshow('no line',lineOut)
    # cv2.waitKey()

    ksize = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
    lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_CLOSE,kernel)
    #lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_OPEN,kernel)

    # cv2.imshow('morphed',lineOut)
    # cv2.waitKey()
    song_durations = []
    _, notes = cv2.threshold(lineOut,200,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('Inv', notes)
    cv2.waitKey()
    num_labels_black, labels_img_black, stats_black, centroids_black = cv2.connectedComponentsWithStats(cv2.bitwise_not(notes))
    staff_tol = 25
    for stat in stats_black:
        x0 = stat[cv2.CC_STAT_LEFT]
        y0 = stat[cv2.CC_STAT_TOP]
        x1 = x0 + stat[cv2.CC_STAT_WIDTH]
        y1 = y0 + stat[cv2.CC_STAT_HEIGHT]
        if (min(lineLocs)-y0<staff_tol) and (y1-max(lineLocs)<staff_tol) and stat[cv2.CC_STAT_WIDTH]>3:
            # match = findBestMatch(notes[y0:y1,x0:x1])
            # print(match)
            cv2.rectangle(img,(x0,y0),(x1,y1),(255,0,0))
        # else:
        #     cv2.rectangle(img, (x0, y0), (x1, y1), (255, 0, 255))
    cv2.imshow("Black Connected Components",img)
    cv2.waitKey()

if __name__ == '__main__':
    notesTest()