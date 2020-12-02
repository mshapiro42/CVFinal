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
#cv2.waitKey()
cv2.imwrite("sharp.jpg",sharp)

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
cv2.waitKey()
cv2.imwrite("fourfour.jpg",fourfour)


