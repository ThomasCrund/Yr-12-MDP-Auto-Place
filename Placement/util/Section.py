import math
from Placement.util.CustomMath import getAngle, getLength
import cv2 as cv


class Section:

    adjMin = None
    adjMax = None
    adjMaxPt = (0, 0)
    adjMinPt = (0, 0)
    SpaceMaxPt = (0, 0)
    SpaceMinPt = (0, 0)

    def __init__(self, offsetX, offsetY, angle, originalSide):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.angle = angle
        self.originalSide = originalSide
        pass

    def setAdjacent(self, direction, num):
        if direction == 1:
            self.adjMax = num
            self.adjMaxPt = ( int( self.offsetX + num * math.cos(self.angle)), int( self.offsetY + num * math.sin(self.angle)) )
        else:
            self.adjMin = num
            self.adjMinPt = ( int( self.offsetX + num * math.cos(self.angle)), int( self.offsetY + num * math.sin(self.angle)) )
    
    def setSpace(self, direction, num):
        if direction == 1:
            self.SpaceMax = num
            self.SpaceMaxPt = ( int( self.offsetX + num * math.cos(self.angle)), int( self.offsetY + num * math.sin(self.angle)) )
        else:
            self.SpaceMin = num
            self.SpaceMinPt = ( int( self.offsetX + num * math.cos(self.angle)), int( self.offsetY + num * math.sin(self.angle)) )

    def getPoints(self):
        return self.adjMinPt, self.adjMaxPt, self.SpaceMinPt, self.SpaceMaxPt

    def exists(self):
        return not (self.adjMin == None or self.adjMax == None)






def createSection(section, pointA, pointB, offsetDistance, cutouts, currentCutoutIndex, screen):
    secondAccuracy = 1
    aX, aY = pointA
    length = getLength(pointA, pointB)
    angle = getAngle(pointA, pointB)
    width, height = screen

    along = int((section[0] + section[1])/ 2)

    offsetStartX = aX + offsetDistance * math.cos(angle + (math.pi / 2))
    offsetStartY = aY + offsetDistance * math.sin(angle + (math.pi / 2))
    checkDistance = cv.pointPolygonTest(cutouts[currentCutoutIndex].points, (offsetStartX + along * math.cos(angle), offsetStartY + along * math.sin(angle)), False)
    # print(checkDistance, offsetStartX, offsetStartY, currentCutoutIndex)
    if checkDistance > 0:
        # print("changedSides")
        offsetStartX = aX + offsetDistance * math.cos(angle - (math.pi / 2))
        offsetStartY = aY + offsetDistance * math.sin(angle - (math.pi / 2))


    sectionData = Section(offsetStartX, offsetStartY, angle, (pointA, pointB))

    direction = 1
    while direction >= 0:
        if direction == 1:
            along += secondAccuracy
        else:
            along -= secondAccuracy
        pointX = int( offsetStartX + along * math.cos(angle))
        pointY = int( offsetStartY + along * math.sin(angle))

        interupt = False
        if pointX <= 0 or pointX >= width or pointY <= 0 or pointY >= height:
            interupt = True
            direction -= 1
        if interupt == True: continue
        saveDistance = 0
        saveId = 0
        for i in range(len(cutouts)):
            distance = cv.pointPolygonTest(cutouts[i].points, (pointX, pointY), True)
            if distance > -(offsetDistance - 2):
            # if distance < (offsetDistance - 1):
                saveDistance = distance
                saveId = i
                interupt = True
                direction -= 1
                break
        # print(interupt, along, pointX, pointY, direction)
        if interupt == True: 
            # print(along, saveDistance, saveId, pointX, pointY)
            pass
            
        if interupt == False:
            if along <= section[1] and along >= section[0]:
                sectionData.setAdjacent(direction, along)
            sectionData.setSpace(direction, along)
    # print(sectionData)
    if sectionData.exists():
        return sectionData
    else:
        return None
        # print(section[0], section[1], offsetStartX, offsetStartY, aX, aY, angle, pointB)

        adjMin, adjMax, spaceMin, spaceMax = sectionData.getPoints()
        # print(adjMin, adjMax)
        # cv.line(img, (int(offsetStartX), int(offsetStartY)), (int( offsetStartX + length * math.cos(angle)), int( offsetStartY + length * math.sin(angle))), (255, 0, 255))
        