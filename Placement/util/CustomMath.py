import math


def getAngle(PointA, PointB):
    return math.atan2( ( PointB[1] - PointA[1] ), ( PointB[0] - PointA[0] ) ) 

def getLength(PointA, PointB):
    return math.sqrt( math.pow(PointB[1] - PointA[1], 2) + math.pow(PointB[0] - PointA[0], 2) )