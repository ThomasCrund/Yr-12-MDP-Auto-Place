import cv2 as cv
import numpy as np
import math
from Placement.util.CustomMath import rotateAroundPoint 

def countourDefault(value):
    return value
class Part:

    Units = {
        "millimeter": 1.0,
        "inch": 25.4
    }

    def __init__(self, unit = Units["millimeter"]):
        self.vertices = []
        self.minX = None
        self.minY = None
        self.maxY = None
        self.maxX = None
        self.unit = unit

    def addPoint(self, point):
        # print(point)
        self.vertices.append(tuple((point[0], point[1])))
        if self.minX == None or self.minX > point[0]: self.minX = point[0]
        if self.minY == None or self.minY > point[1]: self.minY = point[1]
        if self.maxX == None or self.maxX < point[0]: self.maxX = point[0]
        if self.maxY == None or self.maxY < point[1]: self.maxY = point[1]

    def findArea(self):
        n = len(self.vertices) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i][0] * self.vertices[j][1]
            area -= self.vertices[j][0] * self.vertices[i][1]
        area = abs(area) / 2.0
        return area

    def getContour(self, transformFunction = countourDefault):

        def mappingFunction(value):
            x, y = transformFunction(value)
            return [[x, y]]

        return np.array(list(map(mappingFunction, self.vertices)))

    def transformToContour(self):

        yTemp = -self.minY
        self.minY = -self.maxY
        self.maxY = yTemp

        xMove = 0 - self.minX
        yMove = 0 - self.minY

        def mappingFunction(value):
            x, y = value
            y = -y
            return (round(x + xMove), round(y + yMove))

        self.vertices = list(map(mappingFunction, self.vertices))
        
        self.maxX = round(self.maxX + xMove)
        self.minX = round(self.minX + xMove)
        self.minY = round(self.minY + yMove)
        self.maxY = round(self.maxY + yMove)

    def positiveContour(self):

        xMove = 0 - self.minX
        yMove = 0 - self.minY

        def mappingFunction(value):
            x, y = value
            return (round(x + xMove), round(y + yMove))

        self.vertices = list(map(mappingFunction, self.vertices))
        
        self.maxX = round(self.maxX + xMove)
        self.minX = round(self.minX + xMove)
        self.minY = round(self.minY + yMove)
        self.maxY = round(self.maxY + yMove)


    def print(self, border = 5):
        img = np.ones((self.maxY, self.maxX, 3), np.uint8)*255
        

        cv.drawContours(img, [self.getContour()], -1, (0, 255, 0), 2, cv.LINE_8)

        # cv.imwrite('OutputImage.jpg', img)
        cv.imshow('Material Print', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def rotate(self, point, angle):
        newPart = Part(self.unit)
        for vertex in self.vertices:
            newPart.addPoint(rotateAroundPoint(vertex, angle, point))
        newPart.positiveContour()
        return newPart
        


    