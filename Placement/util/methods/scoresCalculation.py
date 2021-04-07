from Placement.util.Material import Material
from Placement.util.Part import Part
from Placement.util.methods.ImageOutput import generateImg, displayImage

# from Placement.util.CustomMath import getAngle, getLength
import numpy as np
import cv2 as cv

# withoutScores = {}

def calculatePerimeter(mat: Material, placedPart: Part, nearby, debug = False):

    adjArray = np.array([[[0, 0]]])
    individualPerimeters = []
    noneNearby = False
    # withoutCode = ""
    for i in range(len(mat.cutouts)):
        if nearby[i] < 30:
            if debug: print(i, nearby[i])
            # withoutCode += str(i)
            noneNearby = True
            adjArray = np.concatenate((adjArray, mat.cutouts[i].points))
            individualArray = np.concatenate((mat.cutouts[i].points, placedPart.getContour()))
            individualPerimeters.append(( cv.arcLength( cv.convexHull( mat.cutouts[i].points ), True ) , cv.arcLength( cv.convexHull( individualArray ), True ) ))
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
     
    # print(noneNearby, nearby, permimeterWith, permimeterWithout, permimeterWith - permimeterWithout)
    totalPerimeterScore = 100
    if permimeterWith != permimeterWithout: 

        totalPerimeterScore = cv.arcLength(placedPart.getContour(), True) / ( permimeterWith - permimeterWithout )

    adjustmentScore = 1 / averagePerimeters(individualPerimeters)

    if debug: 
        print(permimeterWithout, permimeterWith, cv.arcLength(placedPart.getContour(), True), totalPerimeterScore, adjustmentScore)
        img = generateImg(mat.height, mat.width)


        cv.drawContours(img, [hullWithout], -1, (0, 255, 0), 2, cv.LINE_8)
        cv.drawContours(img, [hullWith], -1, (0, 0, 255), 2, cv.LINE_8)
        cv.drawContours(img, [placedPart.getContour()], -1, (255, 0, 0), 2, cv.LINE_8)


        cv.imwrite("OutputImageDebug.jpg", img)
        print(individualPerimeters)


    return totalPerimeterScore * adjustmentScore

def averagePerimeters(perimeters):
    adder = 0
    for i in range( len( perimeters ) ):
        adder += (perimeters[i][1] - perimeters[i][0])

    return adder / len(perimeters)