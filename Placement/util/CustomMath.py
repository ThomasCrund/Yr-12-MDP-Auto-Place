import math


def getAngle(PointA, PointB):
    return math.atan2( ( PointB[1] - PointA[1] ), ( PointB[0] - PointA[0] ) ) 

def getLength(PointA, PointB):
    return math.sqrt( math.pow(PointB[1] - PointA[1], 2) + math.pow(PointB[0] - PointA[0], 2) )

def rotateAroundPoint(PointA, angle, PointB = (0, 0)):
    PointToRotate = (PointA[0] - PointB[0], PointA[1] - PointB[1])
    xNew = round(PointToRotate[0] * math.cos(angle) - PointToRotate[1] * math.sin(angle))
    yNew = round(PointToRotate[1] * math.cos(angle) + PointToRotate[0] * math.sin(angle))
    return (xNew + PointB[0], yNew + PointB[1])

def average(list):
    return sum(list) / len(list)