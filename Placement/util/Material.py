from Placement.util.Cutout import Cutout
from Placement.util.Section import Section, createSection
from Placement.util.CustomMath import getAngle, getLength
import cv2 as cv
import numpy as np
import random as rnd
import math

class Material:

    cutouts = None

    def __init__(self, materialCutouts, height, width):
        self.cutouts = materialCutouts
        self.height = height
        self.width = width

    def print(self):
        img = np.ones((self.height, self.width, 3), np.uint8)*255
        for cutout in self.cutouts:
            color = (rnd.randint(0,256), rnd.randint(0,256), rnd.randint(0,256))
            cv.drawContours(img, [cutout.getPoints()], -1, color, 2, cv.LINE_8)
        sections = self.findSections(16, 5)
        for Section in sections:
            adjMin, adjMax, spaceMin, spaceMax = Section.getPoints()
            cv.line(img, spaceMin, spaceMax, (0, 255, 0))
            cv.line(img, adjMin, adjMax, (0, 0, 255))

        # cv.imwrite('OutputImage.jpg', img)
        cv.imshow('Material Print', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def displayOnImage(self, img, sectionsShow = True):
        for cutout in self.cutouts:
            color = (rnd.randint(0,256), rnd.randint(0,256), rnd.randint(0,256))
            cv.drawContours(img, [cutout.getPoints()], -1, color, 1, cv.LINE_8)
        if sectionsShow:
            sections = self.findSections(16, 5)
            for Section in sections:
                adjMin, adjMax, spaceMin, spaceMax = Section.getPoints()
                cv.line(img, spaceMin, spaceMax, (0, 255, 0))
                cv.line(img, adjMin, adjMax, (0, 0, 255))
        return img


    def getCutouts(self):
        return self.cutouts

    def findSections(self, offsetDistance, accuracy = 5, secondAccuracy = 1):
        # img = np.ones((self.height, self.width, 3), np.uint8)*255
        # cv.line(img, (239, 165), (int( 239 + 50 * math.cos(-2.35619)), int( 165 + 50 * math.sin(-2.35619))), (255, 0, 255))
        materialSections = []
        previousSection = None

        
        def callback(pointA, pointB, currentCutoutIndex):

            length = getLength(pointA, pointB)
            angle = getAngle(pointA, pointB)
            # print(pointA, pointB)
            # print(pointA, pointB, math.degrees(angle), length)
            aX, aY = pointA
            openSections = []
            open = False
            # print(math.ceil(length / accuracy) + 1)
            

            for i in range(math.ceil(length / accuracy) + 1):
                lengthAlong = i * accuracy
                # print(lengthAlong)
                pointX, pointY = pointB
                if lengthAlong < length: 
                    pointX = int( aX + lengthAlong * math.cos(angle))
                    pointY = int( aY + lengthAlong * math.sin(angle))
                else:
                    lengthAlong = length
                smallest = -1000
                smallestId = 0
                for i in range(len(self.cutouts)):
                    if i == currentCutoutIndex: continue
                    distance = cv.pointPolygonTest(self.cutouts[i].points, (pointX, pointY), True)
                    if (distance > smallest): 
                        smallest = distance
                        smallestId = i
                if smallest < -(offsetDistance * 2):
                    if open == False:
                        open = True
                        openSections.append([lengthAlong, lengthAlong])
                    else:
                        openSections[-1][1] = lengthAlong
                    # cv.circle(img, (pointX, pointY), 1, (0, 255, 0))
                    # img[pointY][pointX] = [0, 255, 0]

                else:
                    open = False
                    # print("Distance", smallest, smallestId)
            # nonlocal previousSection
            # print(pointA, pointB, openSections, currentCutoutIndex)
            # if len(openSections) == 0:
            # cv.putText(img, str(pointA[0]) + "," + str(pointA[1]), (pointA[0], pointA[1]), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0))
            # cv.circle(img, (pointA[0], pointA[1]), 1, (0, 255, 0))
            # cv.putText(img, str(pointB[0]) + "," + str(pointB[1]), (pointB[0], pointB[1]), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0))
            # cv.circle(img, (pointB[0], pointB[1]), 1, (0, 255, 0))
            for currentSectionId in range(len(openSections)):
                section = openSections[currentSectionId]
            
                sectionData = createSection(section, pointA, pointB, offsetDistance, self.cutouts, currentCutoutIndex, (self.width, self.height), currentCutoutIndex)
                if sectionData != None:
                    materialSections.append(sectionData)
                
                    # cv.line(img, adjMin, adjMax, (0, 0, 255))
            # print("sections", sideSections)

        for i in range(len(self.cutouts)):
            self.cutouts[i].forSide(lambda a, b: callback(a, b, i))
        # self.cutouts[8].forSide(lambda a, b: callback(a, b, 8))
        
        # img[165][239] = [255, 0, 0]
        # img[150][252] = [255, 0, 0]
        # img[164][238] = [255, 0, 0]
        # cv.circle(img, (239, 165), 1, (255, 0, 0))
        # cv.circle(img, (252, 150), 1, (255, 0, 0))
        
        # cv.imwrite('OutputImagePoints.jpg', img, )
        # cv.imshow('Find Sections', img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()  

        return materialSections