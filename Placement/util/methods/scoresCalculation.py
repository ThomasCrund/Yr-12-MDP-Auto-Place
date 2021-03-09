from Placement.util.Material import Material
from Placement.util.Part import Part
# from Placement.util.CustomMath import getAngle, getLength
import numpy as np
import cv2 as cv

# withoutScores = {}

def calculatePerimeter(mat: Material, placedPart: Part, nearby):

    adjArray = np.array([[[0, 0]]])
    noneNearby = False
    # withoutCode = ""
    for i in range(len(mat.cutouts)):
        if nearby[i] < 23:
            # withoutCode += str(i)
            noneNearby = True
            adjArray = np.concatenate((adjArray, mat.cutouts[i].points))
    adjArray = np.delete(adjArray, 0, 0)

    if not noneNearby:
        return 0

    # print(adjArray, [ cutout.points for cutout in mat.cutouts], placedPart)
    # print(withoutScores)
    # if not withoutCode in withoutScores:
    hullWithout = cv.convexHull(adjArray)
    # withoutScores[withoutCode] = cv.arcLength(hullWithout, True)
    permimeterWithout = cv.arcLength(hullWithout, True)
    # permimeterWithout = withoutScores[withoutCode]

    adjArray = np.concatenate((adjArray, placedPart.getContour()))

    hullWith = cv.convexHull(adjArray)
    permimeterWith = cv.arcLength(hullWith, True)
     

    # print(permimeterWithout, permimeterWith, permimeterWithout / permimeterWith)



    return permimeterWithout / permimeterWith