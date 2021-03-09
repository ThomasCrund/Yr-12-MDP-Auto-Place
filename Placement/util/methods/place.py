from Placement.util.Material import Material
from Placement.util.Part import Part
from Placement.util.CustomMath import getAngle, getLength, average
from Placement.util.methods.ImageOutput import generateImg, displayImage
from Placement.util.methods.scoresCalculation import calculatePerimeter
import math
import cv2 as cv

def placePerimeter(mat: Material, part: Part):
    # mat.print()
    # part.print()
    bestScore = 0
    bestPartPlacement = None

    sections = mat.findSections(20)
    for section in sections:
        # print(section.getPoints(), section.placeSide)
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


            # print(mat.height, mat.width)

            # cv.line(img, section.SpaceMinPt, section.SpaceMaxPt, (255, 0, 0))
            # cv.circle(img, section.SpaceMaxPt, 2, (0, 255, 0), 1)

            # print(PartSectionAngle, sectionAngle, sectionAngle - PartSectionAngle + math.pi)
            # print(PartSectionAngle * 180/math.pi, sectionAngle * 180/math.pi, (sectionAngle - PartSectionAngle + math.pi) * 180/math.pi)
            PartRotated = part.rotate(PointA, sectionAngle - PartSectionAngle + math.pi)

            PointARot = PartRotated.vertices[partSideId]
            PointBRot = PartRotated.vertices[nextSideId]

            if PartSectionLength > maxLength: continue
            if PartSectionLength <= 2: continue

            # print("#####", section.adjMin, section.adjMax, section.SpaceMin, section.SpaceMax )

            endPoint = section.adjMaxPt
            startPoint = section.adjMinPt
            # print(section.SpaceMin)
            startLength = 0
            if section.SpaceMin < section.adjMin:
                
                if section.SpaceMin < section.adjMin - PartSectionLength:
                    startLength = -PartSectionLength
                    startPoint = ( int( section.adjMinPt[0] + (-PartSectionLength) * math.cos(sectionAngle)), int( section.adjMinPt[1] + (-PartSectionLength) * math.sin(sectionAngle)) )
                else:
                    startLength = section.SpaceMin
                    startPoint = section.SpaceMinPt

            # print(startPoint, endPoint, section.adjMinPt, PartSectionLength, PartSectionAngle * 180 / math.pi, sectionAngle * 180 / math.pi)

            testAreaLength = getLength(startPoint, endPoint)
            testPoints = [x / 100 for x in range(0, int(testAreaLength*100), int((testAreaLength*100) / ((testAreaLength)/ 4)))]
            testPoints.append(testAreaLength)
            for pointLength in testPoints:
                # pointActualLength = pointLength + startLength
                testPoint = ( int( startPoint[0] + pointLength * math.cos(sectionAngle)), int( startPoint[1] + pointLength * math.sin(sectionAngle)) )
                # print(pointLength, startLength, testAreaLength, testPoint, section.placeSide)

                PartMoved = PartRotated.copyMove(testPoint[0] - PointARot[0], testPoint[1] - PointARot[1], mat.width, mat.height)
                if PartMoved == None:
                    continue
                # img = generateImg(mat.height, mat.width)

                # img = mat.displayOnImage(img)
                # cv.drawContours(img, [PartMoved.getContour()], -1, (0, 255, 0), 2, cv.LINE_8)
                # cv.line(img, section.SpaceMinPt, section.SpaceMaxPt, (255, 0, 0))
                # cv.circle(img, startPoint, 2, (0, 0, 0), 2)
                # cv.circle(img, endPoint, 2, (0, 255, 0), 1)

                sectionDistances = {}
                for i in range(len(mat.cutouts)):
                    sectionDistances[i] = 99999999.9

                safePlace = True
                for partSideCheckId in range(vertexLength):
                    nextSideCheckId = partSideCheckId + 1
                    if nextSideCheckId == vertexLength: nextSideCheckId = 0
                    PointCheckA = PartMoved.vertices[partSideCheckId]
                    PointCheckB = PartMoved.vertices[nextSideCheckId]
                    
                    CheckAngle = getAngle(PointCheckA, PointCheckB)
                    CheckLength = getLength(PointCheckA, PointCheckB)

                    pointCheck = PointCheckA
                    for cutoutId in range(len(mat.cutouts)):
                        cutout = mat.cutouts[cutoutId]
                        distance = -cv.pointPolygonTest(cutout.points, pointCheck, True)
                        if sectionDistances[cutoutId] > distance:
                            sectionDistances[cutoutId] = distance

                        if distance > 18 + CheckLength:
                            pass
                            # cv.circle(img, pointCheck, abs(int(distance)), (0, 255, 0), 1)
                        elif distance > 18:
                            # print(partSideCheckId, pointCheck, distance, CheckLength, CheckLength + 18)
                            # cv.circle(img, pointCheck, abs(int(distance)), (255, 0, 0), 1)
                            checking = True
                            remainingLength = CheckLength
                            pointCheckNew = PointCheckA
                            while checking:
                                pointCheckNew = ( int( pointCheckNew[0] + distance * math.cos(CheckAngle)), int( pointCheckNew[1] + distance * math.sin(CheckAngle)) )
                                # print(partSideCheckId, pointCheck, distance, CheckLength, CheckLength + 18)
                                distance = -cv.pointPolygonTest(cutout.points, pointCheckNew, True)

                                if sectionDistances[cutoutId] > distance:
                                    sectionDistances[cutoutId] = distance
                                # cv.circle(img, pointCheckNew, abs(int(distance)), (255, 0, 0), 1)
                                if distance < 18:
                                    safePlace = False
                                    break
                                    # cv.circle(img, pointCheckNew, abs(int(distance)), (0, 0, 255), 1)

                                remainingLength -= distance
                                if distance > remainingLength + 18:
                                    checking = False

                        else:
                            safePlace = False
                            break
                            # cv.circle(img, pointCheck, abs(int(distance)), (0, 0, 255), 1)
                            print("Can't Fit", partSideCheckId, pointCheck, distance, CheckLength, CheckLength + 18)

                        if safePlace == False: break
                    if safePlace == False: break
                
                if safePlace == False: continue

                # print(PointA, (sectionAngle - PartSectionAngle + math.pi), PointARot, testPoint, sectionDistances)
                # if average([sectionDistances[i] for i in range(len(mat.cutouts))]) < 22:
                # displayImage(img)
                # print(PartMoved)
                # score = 1
                score = calculatePerimeter(mat, PartMoved, sectionDistances)
                # print(score)

                if score > bestScore:
                    bestScore = score
                    bestPartPlacement = PartMoved



    img = generateImg(mat.height, mat.width)

    img = mat.displayOnImage(img)

    cv.drawContours(img, [bestPartPlacement.getContour()], -1, (0, 255, 0), 2, cv.LINE_8)

    cv.imwrite("OutputImage.jpg", img)

    # displayImage(img)






    return (0, 0, 0)