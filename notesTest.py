import cv2
import numpy as np
import math
import musicalbeeps
from clefFind import *
from Lineout import *
from keyGet import *


def createThreshTemp(img, inv):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if inv:
        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
    else:
        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    return img


def calcStaffInd(lineLocs):
    lineLocs = np.array(lineLocs)
    indx = np.zeros(11)

    for i in range(5):
        indx[1+2*i] = lineLocs[4-i]
    for i in range(1,5):
        indx[2*i] = abs(indx[2*i+1]  + indx[2*i-1])//2
    indx[0] = indx[1] + (indx[1]-indx[2]) - 3
    indx[10] = indx[9] - (indx[8] - indx[9])
    return indx

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
    ksize = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Sig",img)
    # cv2.waitKey(30)
    tempF = cv2.imread('flat.jpg')
    tempF = createThreshTemp(tempF, True)
    # cv2.imshow("Flat template",tempF)

    tempS = cv2.imread('sharp.jpg')
    tempS = createThreshTemp(tempS, True)
    # cv2.imshow("Sharp template",tempS)

    flatFind = cv2.matchTemplate(img,tempF,cv2.TM_CCOEFF_NORMED)
    hitF = np.amax(flatFind)
    # cv2.imshow("Flat matches",flatFind)
    numF = sum(sum(flatFind>(.999*hitF)))
    sharpFind = cv2.matchTemplate(img,tempS,cv2.TM_CCOEFF_NORMED)
    # cv2.imshow("Sharp matches", sharpFind)
    # cv2.waitKey(30)
    hitS = np.amax(sharpFind)
    numS = sum(sum(sharpFind>(.95*hitS)))

    if hitF > hitS:
        key = "flat"
        numS = 0
    else:
        key = "sharp"
        numF = 0
    return(numS, numF)


def findBestMatch(note):
    length = -1
    m = .1
    n = .5
    l = .25
    hits = np.zeros(7)

    ksize = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    note = cv2.morphologyEx(note, cv2.MORPH_OPEN, kernel)
    note = cv2.morphologyEx(note, cv2.MORPH_CLOSE, kernel)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    params.blobColor = 0
    params.blobColor = 255
    whiteBlobDetector = cv2.SimpleBlobDetector_create(params)

    white_blobs = whiteBlobDetector.detect(note)
    # im_with_keypoints = cv2.drawKeypoints(note, white_blobs, np.array([]), (0, 0, 255),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("Keypoints", im_with_keypoints)
    # cv2.waitKey(30)

    if len(white_blobs) != 0:
        if(note.shape[1]>=eighth1.shape[1] and note.shape[0]>=eighth1.shape[0]):
            hits[0] = np.amax(cv2.matchTemplate(note, eighth1, cv2.TM_CCOEFF_NORMED))
        if (note.shape[1] >= eighth2.shape[1] and note.shape[0] >= eighth2.shape[0]):
            hits[1] = np.amax(cv2.matchTemplate(note, eighth2, cv2.TM_CCOEFF_NORMED))
        if (note.shape[1] >= quarter1.shape[1] and note.shape[0] >= quarter1.shape[0]):
            hits[2] = np.amax(cv2.matchTemplate(note, quarter1, cv2.TM_CCOEFF_NORMED))
            hits[3] = np.amax(cv2.matchTemplate(note, quarter2, cv2.TM_CCOEFF_NORMED))
    else:
        if(note.shape[1]>=half1.shape[1] and note.shape[0]>=half1.shape[0]):
            hits[4] = np.amax(cv2.matchTemplate(note, half1, cv2.TM_CCOEFF_NORMED))
            hits[5] = np.amax(cv2.matchTemplate(note, half2, cv2.TM_CCOEFF_NORMED))
        if (note.shape[1] >= whole.shape[1] and note.shape[0] >= whole.shape[0]):
            hits[6] = np.amax(cv2.matchTemplate(note, whole, cv2.TM_CCOEFF_NORMED))

    #
    #print(hits)
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
        length = i
    if length==-1:
        return 0, stemDir
    elif (length==0 or length==1):
        return 1, stemDir
    elif (length==2 or length==3):
        return 2, stemDir
    elif (length==4 or length==5):
        return 3, stemDir
    else:
        return 4, stemDir


def findClosest(array,val):
    diff = abs(array - val)
    i = np.argmin(diff)
    val2 = array[i]
    return i, val2


def findAccidentals(img):
    if img.shape[1]>45:
        # cv2.imshow("Sig",img)
        # cv2.waitKey(30)
        tempF = cv2.imread('flat.jpg')
        tempF = createThreshTemp(tempF, True)
        #cv2.imshow("Flat template",tempF)

        tempS = cv2.imread('sharp.jpg')
        tempS = createThreshTemp(tempS, True)
        #cv2.imshow("Sharp template",tempS)


        tempN = cv2.imread('natural.jpg')
        tempN = createThreshTemp(tempN, True)
        #cv2.imshow("Natural template",tempN)

        flatFind = cv2.matchTemplate(img,tempF,cv2.TM_CCOEFF_NORMED)
        # cv2.imshow("Flat match",flatFind)
        hitF = np.amax(flatFind)
        sharpFind = cv2.matchTemplate(img,tempS,cv2.TM_CCOEFF_NORMED)
        # cv2.imshow("Sharp match",sharpFind)
        hitS = np.amax(sharpFind)
        naturalFind = cv2.matchTemplate(img, tempN, cv2.TM_CCOEFF_NORMED)
        # cv2.imshow("Sharp match",sharpFind)
        hitN = np.amax(naturalFind)
        # cv2.waitKey(30)
        if hitN < .55:
            if hitF>.55:
                tone = -1
            elif hitS>.55:
                tone = 1
            else:
                tone = 0
        else:
            tone = 0
    else:
        tone = 0
    return tone




def playCalced(durations,notes):
    player = musicalbeeps.Player(volume=0.3,
                                 mute_output=False)
    # Examples:
    tempo = 60 # beats per minute
    spb = 60/tempo # seconds per beat
    for i in range(len(notes)):
        player.play_note(notes[i], spb * durations[i])


def notesTest(img_name):
    img = cv2.imread(img_name)
    imgGr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image_width = img.shape[1]
    image_height = img.shape[0]

    # cv2.imshow("Gray Image",imgGr)
    _,imgGr = cv2.threshold(imgGr,200,255,cv2.THRESH_BINARY_INV)

    # cv2.imshow("Thresh Image",imgGr)
    lineOut, lineLocs = lineout(imgGr)

    indx = calcStaffInd(lineLocs)
    clef = clefFind(imgGr)
    cv2.putText(img,clef,(10,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0))
    print(clef)
    print(indx)
    ksize = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ksize,ksize))
    lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_CLOSE,kernel)
    #lineOut = cv2.morphologyEx(lineOut,cv2.MORPH_OPEN,kernel)

    # cv2.imshow('morphed',lineOut)
    # cv2.waitKey()
    song_durations = []
    note_positions = []
    _, notes = cv2.threshold(lineOut,200,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow('Inv', notes)
    # cv2.waitKey()

    num_labels_black, labels_img_black, stats_black, centroids_black = cv2.connectedComponentsWithStats(cv2.bitwise_not(notes))
    #num_labels_black, labels_img_black, stats_black, centroids_black = cv2.connectedComponentsWithStats(notes)
    staff_tol = 25
    objects = []
    centers = []
    noteNames = []
    noteNamesAcc = []
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
        # cv2.imshow("Black Connected Components",object_img)
    # cv2.waitKey()

    o = objects[0]
    if isTimeSig(np.copy(imgGr[o[1]:o[3], o[0]-5:o[2]+5])):
        del objects[0]
        numS,numF = 0, 0
    else:
        numS,numF = findKey(np.copy(imgGr[o[1]-7:o[3]+7, o[0]-5:o[2]+5]))
        del objects[0:2], centers[0:2]
    print(numS,numF)
    key = keyGet(clef,numS,numF)
    if numF>0:
        string = f"{numF} flat"
        if numF>1:
            string += 's'
        cv2.putText(img,string,(50,130),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0))
    elif numS>0:
        string = f"{numS} sharp"
        if numS>1:
            string += 's'
        cv2.putText(img, string, (50, 130), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))
    print(key)
    #print(objects)
    for i, o  in enumerate(objects):
        #note = np.copy(imgGr[max(o[5]-40,0):min(o[5]+40,image_height),max(o[4]-22,0):min(o[4]+22,image_width)])
        note = np.copy(imgGr[o[1]-7:o[3]+7, o[0]-7:o[2]+7])
        type, stemDir = findBestMatch(note)

        if stemDir:
            pos = o[1]+5 #note center is top + 11 pixels
        else:
            pos = o[1]+42 # note center is top +50 pixels
        if type==4:
            pos = o[5] # whole note position is 5 from top
        note_positions.append(findClosest(indx,pos)[0])

        tone = findAccidentals(np.copy(imgGr[o[1]-7:o[3]+7, o[0]-7:o[2]+7]))
        if clef =='Treble':
            noteNames.append(trebChrom[key[note_positions[-1]]])
            noteNamesAcc.append(trebChrom[key[note_positions[-1]]+tone])
        elif clef == 'Bass':
            noteNames.append(bassChrom[key[note_positions[-1]]+tone])
            noteNamesAcc.append(bassChrom[key[note_positions[-1]]+tone])
        song_durations.append(pow(2,-(4-type)))
        #print(noteNames[type],stemDir,song_durations[-1])
        cv2.rectangle(img, (o[0], o[1]), (o[2], o[3]), colors[type])
        cv2.putText(img,noteNamesAcc[-1],(o[0]-4,35),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0))
        cv2.imshow("Note Types",img)
        cv2.waitKey(10)
    print(song_durations)
    # print(noteNames)
    print(noteNamesAcc)
    cv2.waitKey()
    return img, song_durations, noteNamesAcc

trebChrom = ['C4#','D4', 'D4#','E4','F4','F4#','G4','G4#','A4','A4#','B4','C5','C5#','D5', 'D5#','E5','F5','F5#','G5','G5#']
bassChrom = ['E2','F2','F2#','G2','G2#','A2','A2#','B2','C3','C3#','D3', 'D3#','E3','F3','F3#','G3','G3#','A3','A3#','B3','C4']

eighth1 = cv2.imread("eighth-1.jpg")
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
# cv2.imshow("Eighth1",eighth1)
# cv2.imshow("eighth2",eighth2)
# cv2.imshow("quarter1",quarter1)
# cv2.imshow("quarter2",quarter2)
# cv2.imshow("half1",half1)
# cv2.imshow("half2",half2)
# cv2.imshow("whole",whole)
# cv2.waitKey()
# cv2.destroyAllWindows()
durations = [0.125,0.25,0.5,1]
colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255),(255,255,0)]
noteNames = ["Unknown","1/8","1/4","1/2","1"]

if __name__ == '__main__':
    for i in range(1,4):
        name = 'mySimpleSong' + str(i) + '.jpg'
        img, durations, notes = notesTest(name)
        name2 = 'mySimpleSong' + str(i) + '-solved.jpg'
        cv2.imwrite(name2,img)
        playCalced(durations,notes)