import numpy as np
import cv2
import os

# Mouse callback function. Appends the x,y location of mouse click to a list.
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        param.append(x)
        param.append(y)

song = cv2.imread("mySimpleSong1.jpg")
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
eighth = cv2.imread("eighth-1.jpg")
scale = 60/eighth.shape[0]
width = round(eighth.shape[1] * scale)
height = round(eighth.shape[0] * scale)
print(scale)
eighth = cv2.resize(src=eighth, dsize=(width, height))
print(eighth.shape)
# cv2.imshow("Eighth Note",eighth)
# cv2.waitKey()
# cv2.imwrite("eighth-1.jpg",eighth)

#eighth note is 70 pixels tall
eighth2 = cv2.imread("eighth2-1.jpg")
scale = 60/eighth2.shape[0]
width = round(eighth2.shape[1] * scale)
height = round(eighth2.shape[0] * scale)
print(scale)
eighth2 = cv2.resize(src=eighth2, dsize=(width, height))
print(eighth2.shape)
# cv2.imshow("Eighth Note 2",eighth2)
# cv2.waitKey()
# cv2.imwrite("eighth2-1.jpg",eighth2)

#eighthtail is 43 pixels tall
eighthtail = cv2.imread("eighthtail.jpg")
scale = 48/eighthtail.shape[0]
width = round(eighthtail.shape[1] * scale)
height = round(eighthtail.shape[0] * scale)
print(scale)
eighthtail = cv2.resize(src=eighthtail, dsize=(width, height))
print(eighthtail.shape)
# cv2.imshow("Eighth Note Tail",eighthtail)
# cv2.imwrite("eighthtail-1.jpg",eighthtail)

#eighthtail2 is 43 pixels tall
eighthtail2 = cv2.imread("eighthtail2.jpg")
scale = 43/eighthtail2.shape[0]
width = round(eighthtail2.shape[1] * scale)
height = round(eighthtail2.shape[0] * scale)
print(scale)
eighthtail2 = cv2.resize(src=eighthtail2, dsize=(width, height))
print(eighthtail2.shape)
# cv2.imshow("Eighth Note Tail 2",eighthtail2)
# cv2.waitKey()
# cv2.imwrite("eighthtail2-1.jpg",eighthtail2)

#quarter note is 70 pixels tall
quarter = cv2.imread("quarter-1.jpg")
scale = 60/quarter.shape[0]
width = round(quarter.shape[1] * scale)
height = round(quarter.shape[0] * scale)
print(scale)
quarter = cv2.resize(src=quarter, dsize=(width, height))
print(quarter.shape)
# cv2.imshow("Quarter Note",quarter)
# cv2.imwrite("quarter-1.jpg",quarter)

#quarter note is 70 pixels tall
quarter2 = cv2.imread("quarter2-1.jpg")
scale = 60/quarter2.shape[0]
width = round(quarter2.shape[1] * scale)
height = round(quarter2.shape[0] * scale)
print(scale)
quarter2 = cv2.resize(src=quarter2, dsize=(width, height))
print(quarter2.shape)
# cv2.imshow("Quarter Note 2",quarter2)
# cv2.imwrite("quarter2-1.jpg",quarter2)

#half note is 70 pixels tall
half = cv2.imread("half-1.jpg")
scale = 60/half.shape[0]
width = round(half.shape[1] * scale)
height = round(half.shape[0] * scale)
print(scale)
half = cv2.resize(src=half, dsize=(width, height))
print(half.shape)
# cv2.imshow("Half Note",half)
# cv2.imwrite("half-1.jpg",half)

#half note is 70 pixels tall
half2 = cv2.imread("half2-1.jpg")
scale = 60/half2.shape[0]
width = round(half2.shape[1] * scale)
height = round(half2.shape[0] * scale)
print(scale)
half2 = cv2.resize(src=half2, dsize=(width, height))
print(half2.shape)
# cv2.imshow("Half Note 2",half2)
# cv2.waitKey()
# cv2.imwrite("half2-1.jpg",half2)

#whole note is 20 pixels tall
whole = cv2.imread("whole.jpg")
scale = 18/whole.shape[0]
width = round(whole.shape[1] * scale)
height = round(whole.shape[0] * scale)
print(scale)
whole = cv2.resize(src=whole, dsize=(width, height))
print(whole.shape)
# cv2.imshow("Whole",whole)
# cv2.waitKey()
# cv2.imwrite("whole-1.jpg",whole)
