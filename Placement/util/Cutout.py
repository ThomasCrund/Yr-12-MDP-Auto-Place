import cv2 as cv


class Cutout:

    points = None

    def __init__(self, contour):
        self.points = contour

    def getPoints(self):
        return self.points

    def forSide(self, callback):
        for i in range(len(self.points)):
            nextIndex = i + 1
            if nextIndex == len(self.points): nextIndex = 0
            callback(self.points[i][0], self.points[nextIndex][0])
    
    def simplify(self):
        self.points = cv.approxPolyDP(self.points, 2, True)
