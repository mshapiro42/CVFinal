import cv2
import numpy as np
import math
from clefFind import *
from Lineout import *


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
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Object",img)
    #cv2.waitKey()
    if(img.shape[0]>=fourfour.shape[0] and img.shape[1]>=fourfour.shape[1]):
        timeFind = cv2.matchTemplate(img,fourfour,cv2.TM_CCOEFF_NORMED)
        hitT = np.amax(timeFind)
        if hitT > .6:
            return True
    return False


def findKey(img):
    #cv2.imshow("Sig",img)
    #cv2.waitKey(30)
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
    m = .1
    n = .5
    l = .25
    hits = np.zeros(7)

    ksize = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    note = cv2.morphologyEx(note, cv2.MORPH_OPEN, kernel)
    note = cv2.morphologyEx(note, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("Note",note)
    #cv2.waitKey()

    # black = cv2.connectedComponents(note)
    # cv2.imshow("Connected Components", black)
    # circles = cv2.HoughCircles(note, cv2.HOUGH_GRADIENT, 1, 2,
    #                           param1=50, param2=3,
    #                           minRadius=10, maxRadius=20)
    #
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         center = (i[0], i[1])
    #         # circle center
    #         cv2.circle(note, center, 1, (0, 100, 100), 3)
    #         # circle outline
    #         radius = i[2]
    #         cv2.circle(note, center, radius, (255, 0, 255), 3)
    #
    # cv2.imshow("detected circles", note)
    # cv2.waitKey()

    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    params.blobColor = 0
    blackBlobDetector = cv2.SimpleBlobDetector_create(params)
    params.blobColor = 255
    whiteBlobDetector = cv2.SimpleBlobDetector_create(params)

    white_blobs = whiteBlobDetector.detect(note)
    im_with_keypoints = cv2.drawKeypoints(note, white_blobs, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.waitKey(30)
    #
    #
    if len(white_blobs) != 0:
        hits[0] = np.amax(cv2.matchTemplate(note, eighth1, cv2.TM_CCOEFF_NORMED))
        hits[1] = np.amax(cv2.matchTemplate(note, eighth2, cv2.TM_CCOEFF_NORMED))
        hits[2] = np.amax(cv2.matchTemplate(note, quarter1, cv2.TM_CCOEFF_NORMED))
        hits[3] = np.amax(cv2.matchTemplate(note, quarter2, cv2.TM_CCOEFF_NORMED))

    else:
        hits[4] = np.amax(cv2.matchTemplate(note, half1, cv2.TM_CCOEFF_NORMED))
        hits[5] = np.amax(cv2.matchTemplate(note, half2, cv2.TM_CCOEFF_NORMED))
        hits[6] = np.amax(cv2.matchTemplate(note, whole, cv2.TM_CCOEFF_NORMED))

    #
    print(hits)
    if (hits[0] > n or hits[1] > n):
        hits[2:4] = 0
    if (hits[4]>l or hits[5]>l) and hits[6]<.7:
        hits[6] = 0
    #     i = np.argmax(hits[0:4])
    # else:
    #     i = np.argmax(hits[4:len(hits)+1])+4
    i = np.argmax(hits)
    highest = hits[i]
    stemDir = i % 2
    if highest>m:
        best = i
    if best==-1:
        return 0, stemDir
    elif (best==0 or best==1):
        return 1, stemDir
    elif (best==2 or best==3):
        return 2, stemDir
    elif (best==4 or best==5):
        return 3, stemDir
    else:
        return 4, stemDir

def notesTest(img_name):
    img = cv2.imread(img_name)

    imgGr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image_width = img.shape[1]
    image_height = img.shape[0]

    _,imgGr = cv2.threshold(imgGr,200,255,cv2.THRESH_BINARY_INV)

    lineOut, lineLocs = lineout(imgGr)

    clef = clefFind(imgGr)

    print(clef)

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
    #num_labels_black, labels_img_black, stats_black, centroids_black = cv2.connectedComponentsWithStats(notes)
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
            objects.append([x0,y0,x1,y1,round(centroids_black[i,0]),round(centroids_black[i,1])])
        # else:
        #     cv2.rectangle(img, (x0, y0), (x1, y1), (255, 0, 255))
    objects = sorted(objects)
    del objects[0] # Leftmost object is the clef
    del objects[len(objects)-1] # rightmost object is the double end bar
    object_img = np.copy(img)
    for i, o in enumerate(objects):
        cv2.rectangle(object_img, (o[0], o[1]), (o[2], o[3]), (255,0,0))
        cv2.imshow("Black Connected Components",object_img)
    #cv2.waitKey()

    o = objects[0]
    if isTimeSig(np.copy(imgGr[o[1]:o[3], o[0]-5:o[2]+5])):
        del objects[0]
        num,key = 0, "natural"
    else:
        num,key = findKey(np.copy(imgGr[o[1]:o[3], o[0]-5:o[2]+5]))
        del objects[0:2], centers[0:2]
    print(num,key)
    #print(objects)
    for i, o  in enumerate(objects):
        note = np.copy(imgGr[max(o[5]-40,0):min(o[5]+40,image_height),max(o[4]-22,0):min(o[4]+22,image_width)])
        #note = np.copy(img[o[1]:o[3], o[0]-5:o[2]+5])
        type, stemDir = findBestMatch(note)
        print(noteNames[type],stemDir)
        cv2.rectangle(img, (o[0], o[1]), (o[2], o[3]), colors[type])
        cv2.imshow("Black Connected Components",img)
        cv2.waitKey()
    #cv2.waitKey()


eighth1 = cv2.imread("eighthtail-1.jpg")
eighth2 = cv2.imread("eighthtail2-1.jpg")
quarter1 = cv2.imread("quarter-1.jpg")
quarter2 = cv2.imread("quarter2-1.jpg")
half1 = cv2.imread("half-1.jpg")
half2 = cv2.imread("half2-1.jpg")
whole = cv2.imread("whole-1.jpg")

eighth1 = createThreshTemp(eighth1, True)
eighth2 = createThreshTemp(eighth2, True)
quarter1 = createThreshTemp(quarter1, True)
quarter2 = createThreshTemp(quarter2, True)
half1 = createThreshTemp(half1, True)
half2 = createThreshTemp(half2, True)
whole = createThreshTemp(whole, True)

duration = np.array([.125, .125, .25, .25, .5, .5, 1])
colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255),(255,255,0)]
noteNames = ["Unknown","1/8","1/4","1/2","1"]

if __name__ == '__main__':
    for i in range(1,4):
        name = 'mySimpleSong' + str(i) + '.jpg'
        notesTest(name)