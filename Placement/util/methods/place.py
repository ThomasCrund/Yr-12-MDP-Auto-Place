from Placement.util.Material import Material
from Placement.util.Part import Part
from Placement.util.CustomMath import getAngle, getLength
import math

def placePerimeter(mat: Material, part: Part):
    # mat.print()
    # part.print()
    sections = mat.findSections(20)
    for section in sections:
        print(section.getPoints(), section.placeSide)
        sectionAngle = section.angle

        maxLength = getLength(section.SpaceMinPt, section.SpaceMaxPt)
        # print(maxLength)

        vertexLength = len(part.vertices)
        for partSideId in range(vertexLength):
            nextSideId = partSideId + 1
            if nextSideId == vertexLength: nextSideId = 0
            PointA = part.vertices[partSideId]
            PointB = part.vertices[nextSideId]
            
            PartSectionAngle = getAngle(PointA, PointB)
            PartSectionLength = getLength(PointA, PointB)

            # print(sectionAngle, PartSectionAngle)
            # print(maxLength, PartSectionLength)
            if PartSectionLength > maxLength: continue
            if PartSectionLength <= 2: continue

            print(section.adjMin, section.adjMax, section.SpaceMin, section.SpaceMax )

            endPoint = section.adjMaxPt
            startPoint = section.adjMinPt
            # print(section.SpaceMin)
            if section.SpaceMin < section.adjMin:
                
                if section.SpaceMin < section.adjMin - PartSectionLength:
                    startPoint = ( int( section.adjMinPt[0] + (-PartSectionLength) * math.cos(sectionAngle)), int( section.adjMinPt[1] + (-PartSectionLength) * math.sin(sectionAngle)) )
                else:
                    startPoint = section.SpaceMinPt

            print(startPoint, endPoint, section.adjMinPt, PartSectionLength, PartSectionAngle * 180 / math.pi, sectionAngle * 180 / math.pi)

            testAreaLength = getLength(startPoint, endPoint)
            testPoints = [x / 100 for x in range(0, int(testAreaLength*100), int((testAreaLength*100) / ((testAreaLength)/ 4)))]
            testPoints.append(testAreaLength)
            for pointLegnth in testPoints:
                testPoint = ( int( section.adjMinPt[0] + pointLegnth * math.cos(sectionAngle)), int( section.adjMinPt[1] + pointLegnth * math.sin(sectionAngle)) )
                print(pointLegnth, testAreaLength, testPoint)
        






    return (0, 0, 0)