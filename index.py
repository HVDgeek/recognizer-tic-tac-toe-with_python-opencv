import cv2
import numpy as np 
import argparse
import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
clone = image.copy()

for (i , c) in enumerate(cnts):
    #Aspect Ratio
    area = cv2.contourArea(c)
    (x, y , w, h) = cv2.boundingRect(c)

    #Convex Hull
    hull = cv2.convexHull(c)
    hullArea = cv2.contourArea(hull)

    #Solidity
    solidity = area / float(hullArea)

    char = "?"

    if solidity > 0.9:
        char = "O"
    elif solidity > 0.5:
        char = "X"
    
    if char != "?" :
        cv2.drawContours(clone, [c], -1, (0, 255, 0), 2)
        cv2.putText(clone, "{}".format(char), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
            1.25, (0, 255, 0), 3)

    print("{} Contour: #{} ----- Solidity={:.2f}".format(char, i+1, solidity)) 

cv2.imshow('Original', image)
cv2.imshow('Result', clone)
cv2.waitKey(0)