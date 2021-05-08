from Placement.util.Material import Material
from Placement.util.Cutout import Cutout
import cv2 as cv
import random as rng
import numpy as np


def mappingFunction(value):
        x = value['x']
        y = value['y']
        return [[x, y]]

def GenerateMaterialJSON(json):

    height = json["height"]
    width = json["width"]

    cutouts = []
    for contourId in json["cutouts"]:
        contour = json["cutouts"][contourId]


        contourCVStructure = np.array(list(map(mappingFunction, contour)))
        x,y,w,h = cv.boundingRect(contourCVStructure)
        if x == 0 and y == 0 and w == width and h == height: continue # Get Rid of the contour around the border of the image
        cutout = Cutout(contourCVStructure)
        # cutout.simplify()
        # if findDuplicateCutout(cutouts, cutout.points): continue # If duplicate contour exists already do not add this contour
        cutouts.append(cutout)

    m = Material(cutouts, height, width)

    return m