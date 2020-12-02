import cv2
import numpy as np
import math
from clefFind import *


def createThreshTemp(img, inv):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if inv:
        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
    else:
        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    return img


def isTimeSig(img):
    fourfour = cv2.imread("fourfour.jpg")
    fourfour = createThreshTemp(fourfour,True)
    #cv2.imshow("Object",img)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if(img.shape[0]>=fourfour.shape[0] and img.shape[1]>-fourfour.shape[1]):
        timeFind = cv2.matchTemplate(img,fourfour,cv2.TM_CCOEFF_NORMED)
        hitT = np.amax(timeFind)
        if hitT > .6:
            return True
    return False


def findKey(img):
    #cv2.imshow("Sig",img)
    #cv2.waitKey()
    tempF = cv2.imread('flat.jpg')
    tempF = createThreshTemp(tempF, True)
    #cv2.imshow("Flat template",tempF)

    tempS = cv2.imread('sharp.jpg')
    tempS = createThreshTemp(tempS, True)
    #cv2.imshow("Sharp template",tempS)

    flatFind = cv2.matchTemplate(img,tempF,cv2.TM_CCOEFF_NORMED)
    hitF = np.amax(flatFind)
    #cv2.imshow("Flat matches",flatFind)
    numF = sum(sum(flatFind>(.94*hitF)))
    sharpFind = cv2.matchTemplate(img,tempS,cv2.TM_CCOEFF_NORMED)
    #cv2.imshow("Sharp matches", sharpFind)
    #cv2.waitKey()
    hitS = np.amax(sharpFind)
    numS = sum(sum(sharpFind>(.94*hitS)))

    if hitF > hitS:
        key = "flat"
        num = numF
    else:
        key = "sharp"
        num = numS
    return(num,key)


def findBestMatch(note):
    best = -1
    m = .3
    hits = np.zeros(6)
    cv2.imshow("Note",note)
    cv2.waitKey(30)
    hits[0] = np.amax(cv2.matchTemplate(note, eighth1, cv2.TM_CCOEFF_NORMED))
    hits[1] = np.amax(cv2.matchTemplate(note, eighth2, cv2.TM_CCOEFF_NORMED))
    hits[2] = np.amax(cv2.matchTemplate(note, quarter1, cv2.TM_CCOEFF_NORMED))
    hits[3] = np.amax(cv2.matchTemplate(note, quarter2, cv2.TM_CCOEFF_NORMED))
    hits[4] = np.amax(cv2.matchTemplate(note, half1, cv2.TM_CCOEFF_NORMED))
    hits[5] = np.amax(cv2.matchTemplate(note, half2, cv2.TM_CCOEFF_NORMED))

    print(hits)
    i = np.argmax(hits)
    highest = hits[i]
    if highest>m:
        best = i
    if best==-1:
        return 0
    elif (best==0 or best==1):
        return 1
    elif (best==2 or best==3):
        return 2
    elif (best==4 or best==5):
        return 3
    else:
        return best

def notesTest(img_name):
    img = cv2.imread(img_name)

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

    clef = clefFind(imgGr)

    print(clef)
    lineOut = imgGr
    lineLocs = []
    for i in range(len(hough_lines)):
        l = hough_lines[i][0]
        # cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0, 0, 255),
        #          thickness=1, lineType=cv2.LINE_AA)
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
    # cv2.imshow('Inv', notes)
    # cv2.waitKey()

    num_labels_black, labels_img_black, stats_black, centroids_black = cv2.connectedComponentsWithStats(cv2.bitwise_not(notes))
    staff_tol = 25
    objects = []
    centers = []
    for i, stat in enumerate(stats_black):
        x0 = stat[cv2.CC_STAT_LEFT]
        y0 = stat[cv2.CC_STAT_TOP]
        x1 = x0 + stat[cv2.CC_STAT_WIDTH]
        y1 = y0 + stat[cv2.CC_STAT_HEIGHT]
        if (min(lineLocs)-y0<staff_tol) and (y1-max(lineLocs)<staff_tol) and stat[cv2.CC_STAT_WIDTH]>3:
            # match = findBestMatch(notes[y0:y1,x0:x1])
            # print(match)
            objects.append([x0,y0,x1,y1])
            centers.append((round(centroids_black[i,0]),round(centroids_black[i,1])))
        # else:
        #     cv2.rectangle(img, (x0, y0), (x1, y1), (255, 0, 255))
    objects = sorted(objects)
    del objects[0], centers[0] # Leftmost object is the clef
    del objects[len(objects)-1], centers[len(centers)-1] # rightmost object is the double end bar
    o = objects[0]
    if isTimeSig(np.copy(imgGr[o[1]:o[3], o[0]:o[2]])):
        del objects[0], centers[0]
        num,key = 0, "natural"
    else:
        num,key = findKey(np.copy(imgGr[o[1]:o[3], o[0]-5:o[2]+5]))
        del objects[0:2], centers[0:2]
    print(num,key)
    #print(objects)
    for i, o  in enumerate(objects):
        c = centers[i]
        note = np.copy(notes[max(c[1]-40,0):min(c[1]+40,image_height),max(c[0]-25,0):min(c[0]+25,image_width)])
        type = findBestMatch(note)
        cv2.rectangle(img, (o[0], o[1]), (o[2], o[3]), colors[type])
    cv2.imshow("Black Connected Components",img)
    cv2.waitKey()


eighth1 = cv2.imread("eighth.jpg")
eighth2 = cv2.imread("eighth2.jpg")
quarter1 = cv2.imread("quarter.jpg")
quarter2 = cv2.imread("quarter2.jpg")
half1 = cv2.imread("half.jpg")
half2 = cv2.imread("half2.jpg")

eighth1 = createThreshTemp(eighth1, False)
eighth2 = createThreshTemp(eighth2, False)
quarter1 = createThreshTemp(quarter1, False)
quarter2 = createThreshTemp(quarter2, False)
half1 = createThreshTemp(half1, False)
half2 = createThreshTemp(half2, False)

duration = np.array([.125, .125, .25, .25, .5, .5])
colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255)]

if __name__ == '__main__':
    for i in range(1,4):
        name = 'mySimpleSong' + str(i) + '.jpg'
        notesTest(name)