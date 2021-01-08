from Placement.util.Material import Material
from Placement.util.Cutout import Cutout
import cv2 as cv
import random as rng
import numpy as np

def GenerateMaterial(imagePath):
    im = cv.imread(imagePath)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)

    height, width, channels = im.shape

    contours, hierarchy = cv.findContours(blackAndWhiteImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # img = np.ones((height, width, 3), np.uint8)*255

    # for contour in contours:
        
    #     color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #     cv.drawContours(img, [contour], -1, color, 2, cv.LINE_8)

    # cv.imwrite('OutputContours.jpg', img)

    cutouts = []
    for contour in contours:

        x,y,w,h = cv.boundingRect(contour)
        if x == 0 and y == 0 and w == width and h == height: continue # Get Rid of the contour around the border of the image
        cutout = Cutout(contour)
        cutout.simplify()
        if findDuplicateCutout(cutouts, cutout.points): continue # If duplicate contour exists already do not add this contour
        cutouts.append(cutout)

    m = Material(cutouts, height, width)

    return m

def findDuplicateCutout(cutouts, testContour):
    for cutout in cutouts:
        x,y,w,h = cv.boundingRect(cutout.getPoints())
        tx,ty,tw,th = cv.boundingRect(testContour)
        if (tx == x and ty == y) :
            return True
            break
    return False
        