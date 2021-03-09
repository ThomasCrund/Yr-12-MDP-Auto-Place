import cv2 as cv
import numpy as np

def generateImg(height = 600, width = 600):
    return np.ones((height, width, 3), np.uint8)*255

def displayImage(img):
    cv.imshow('image Output', img)
    cv.waitKey(0)
    cv.destroyAllWindows()