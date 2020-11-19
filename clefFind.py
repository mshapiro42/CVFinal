import cv2
import numpy as np

def clefFind(img):
    tempT = cv2.imread('Treble.png')
    tempT = cv2.cvtColor(tempT, cv2.COLOR_BGR2GRAY)
    _, tempT = cv2.threshold(tempT, 200, 255, cv2.THRESH_BINARY_INV)

    tempB = cv2.imread('Bass.png')
    tempB = cv2.cvtColor(tempB, cv2.COLOR_BGR2GRAY)
    _, tempB = cv2.threshold(tempB, 200, 255, cv2.THRESH_BINARY_INV)

    trebFind = cv2.matchTemplate(img,tempT,cv2.TM_CCOEFF_NORMED)
    hitT = np.amax(trebFind)
    bassFind = cv2.matchTemplate(img,tempB,cv2.TM_CCOEFF_NORMED)
    hitB = np.amax(bassFind)

    if hitT > 0.85:
        return "Treble"
    elif hitB > 0.85:
        return "Bass"
    else:
        return "Clef Not Found"
