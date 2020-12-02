import numpy as np
import cv2
import os

# Mouse callback function. Appends the x,y location of mouse click to a list.
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        param.append(x)
        param.append(y)

song = cv2.imread("mySimpleSong3.jpg")
cv2.imshow("Song",song)
# loc = []
# cv2.setMouseCallback("Song", get_xy, loc)
# cv2.waitKey()

def symbols():
    # flat is ~ 19 pixels high
    flat = cv2.imread("flat.jpg")
    #flat = cv2.cvtColor(flat,cv2.COLOR_BGR2GRAY)
    scale = 19/flat.shape[0]
    width = round(flat.shape[1]* scale)
    height = round(flat.shape[0]*scale)
    print(scale)
    flat = cv2.resize(src=flat,dsize=(width,height))
    print(flat.shape)
    cv2.imshow("Flat",flat)
    #cv2.waitKey()
    #cv2.imwrite("flat.jpg",flat)

    # sharp is ~ 26 pixels high
    sharp = cv2.imread("sharp.jpg")
    #flat = cv2.cvtColor(flat,cv2.COLOR_BGR2GRAY)
    scale = 26/sharp.shape[0]
    width = round(sharp.shape[1]* scale)
    height = round(sharp.shape[0]*scale)
    print(scale)
    sharp = cv2.resize(src=sharp,dsize=(width,height))
    print(sharp.shape)
    cv2.imshow("Sharp",sharp)
    # cv2.waitKey()
    # cv2.imwrite("sharp.jpg",sharp)

    # natural is ~ 24 pixels high
    natural = cv2.imread("natural.jpg")
    #flat = cv2.cvtColor(flat,cv2.COLOR_BGR2GRAY)
    scale = 24/natural.shape[0]
    width = round(natural.shape[1]* scale)
    height = round(natural.shape[0]*scale)
    print(scale)
    natural = cv2.resize(src=natural,dsize=(width,height))
    print(natural.shape)
    cv2.imshow("Natural",natural)
    #cv2.waitKey()
    #cv2.imwrite("natural.jpg",natural)

    # fourfour is ~ 48 pixels high
    fourfour = cv2.imread("fourfour.jpg")
    #flat = cv2.cvtColor(flat,cv2.COLOR_BGR2GRAY)
    scale = 48/fourfour.shape[0]
    width = round(fourfour.shape[1]* scale)
    height = round(fourfour.shape[0]*scale)
    print(scale)
    fourfour = cv2.resize(src=fourfour,dsize=(width,height))
    print(fourfour.shape)
    cv2.imshow("Four/Four",fourfour)
    # cv2.waitKey()
    # cv2.imwrite("fourfour.jpg",fourfour)

#eighth note is 70 pixels tall
eighth = cv2.imread("eighth.jpg")
scale = 70/eighth.shape[0]
width = round(eighth.shape[1] * scale)
height = round(eighth.shape[0] * scale)
print(scale)
eighth = cv2.resize(src=eighth, dsize=(width, height))
print(eighth.shape)
# cv2.imshow("Eighth Note",eighth)
# cv2.waitKey()
# cv2.imwrite("eighth.jpg",eighth)

#eighth note is 70 pixels tall
eighth2 = cv2.imread("eighth2.jpg")
scale = 70/eighth2.shape[0]
width = round(eighth2.shape[1] * scale)
height = round(eighth2.shape[0] * scale)
print(scale)
eighth = cv2.resize(src=eighth2, dsize=(width, height))
print(eighth2.shape)
# cv2.imshow("Eighth Note 2",eighth2)
# cv2.waitKey()
# cv2.imwrite("eighth2.jpg",eighth2)

#quarter note is 70 pixels tall
quarter = cv2.imread("quarter.jpg")
scale = 70/quarter.shape[0]
width = round(quarter.shape[1] * scale)
height = round(quarter.shape[0] * scale)
print(scale)
quarter = cv2.resize(src=quarter, dsize=(width, height))
print(quarter.shape)
cv2.imshow("Quarter Note",quarter)
# cv2.imwrite("quarter.jpg",quarter)
# flip quarter template for stem up/down
quarter2 = cv2.rotate(quarter,cv2.ROTATE_180)
cv2.imshow("Quarter 2",quarter2)
# cv2.waitKey()
# cv2.imwrite("quarter2.jpg",quarter2)


# flip half template for stem up/down
half = cv2.imread("half.jpg")
cv2.imshow("Half Note",half)
half2 = cv2.rotate(half,cv2.ROTATE_180)
cv2.imshow("Half 2",half2)
# cv2.waitKey()
# cv2.imwrite("half2.jpg",half2)
