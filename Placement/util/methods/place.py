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
    bestInfo = (0, 0, 0)

    img = generateImg(mat.height, mat.width)

    img = mat.displayOnImage(img, False)

    checkDistance = 17
    sections = mat.findSections(21)
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

            # print(partSideId, PartSectionLength, PartSectionAngle)


            # print(mat.height, mat.width)

            # cv.line(img, section.SpaceMinPt, section.SpaceMaxPt, (255, 0, 0))
            # cv.circle(img, section.SpaceMaxPt, 2, (0, 255, 0), 1)

            # print(PartSectionAngle, sectionAngle, sectionAngle - PartSectionAngle + math.pi)
            # print(PartSectionAngle * 180/math.pi, sectionAngle * 180/math.pi, (sectionAngle - PartSectionAngle + math.pi) * 180/math.pi)
            angleRotated = sectionAngle - PartSectionAngle + math.pi
            PartRotated = part.rotate(PointA, sectionAngle - PartSectionAngle + math.pi)

            PointARot = PartRotated.vertices[partSideId]
            PointBRot = PartRotated.vertices[nextSideId]

            if PartSectionLength > maxLength: continue
            if PartSectionLength <= 2: continue

            # print("#####", section.adjMin, section.adjMax, section.SpaceMin, section.SpaceMax )

            endPoint = section.SpaceMaxPt
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
            # testPoints = [x / 100 for x in range(0, int(testAreaLength*100), int((testAreaLength*100) / ((testAreaLength)/ 4)))]
            # testPoints.append(testAreaLength)
            # testingDistance = min(-PartSectionLength, )

            # if (section.partOffId == 9 and ( partSideId == 5 or partSideId == 11 ) ):
            #     cv.line(img, startPoint, endPoint, (0, 255, 0))
                # cv.line(img, section.SpaceMinPt, section.spaceMaxPt, (0, 255, 0))
                # cv.line(img, section.adjMinPt, section.adjMaxPt, (0, 0, 255))
            
            testingDistance = 0
            while testingDistance < testAreaLength:
            # for pointLength in testPoints:
                # pointActualLength = pointLength + startLength
                testPoint = ( int( startPoint[0] + testingDistance * math.cos(sectionAngle)), int( startPoint[1] + testingDistance * math.sin(sectionAngle)) )
                # print(testingDistance, startLength, testAreaLength, testPoint, section.placeSide)
                xMove = testPoint[0] - PointARot[0]
                yMove = testPoint[1] - PointARot[1]
                PartMoved = PartRotated.copyMove(testPoint[0] - PointARot[0], testPoint[1] - PointARot[1], mat.width, mat.height)
                if PartMoved == None:
                    testingDistance += 4
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
                minDistance = 9999999
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

                        if distance > checkDistance + CheckLength:
                            pass
                            # cv.circle(img, pointCheck, abs(int(distance)), (0, 255, 0), 1)
                        elif distance > checkDistance:
                            # print(partSideCheckId, pointCheck, distance, CheckLength, CheckLength + checkDistance)
                            # cv.circle(img, pointCheck, abs(int(distance)), (255, 0, 0), 1)
                            checking = True
                            remainingLength = CheckLength - checkDistance - distance
                            pointCheckNew = PointCheckA
                            distance -= checkDistance
                            while checking:
                                predistance = distance
                                pointCheckNew = ( int( pointCheckNew[0] + distance  * math.cos(CheckAngle)), int( pointCheckNew[1] + distance * math.sin(CheckAngle)) )
                                # print(partSideCheckId, pointCheck, distance, CheckLength, CheckLength + checkDistance)
                                distance = -cv.pointPolygonTest(cutout.points, pointCheckNew, True)

                                # if ( section.partOffId == 18  and (section.adjMax - section.adjMin) == 153 and ( partSideId == 6 ) and cutoutId == 9 and testingDistance == 185.65957828725098 ): # and distance == 13.408956583091223  and ( partSideId == 5 or partSideId == 11 )
                                #     print(PointCheckA, CheckLength)
                                #     cv.circle(img, PointCheckA, 3, (0, 255, 0), 3)
                                #     print(testingDistance, distance, cutoutId, partSideCheckId, pointCheckNew, predistance, section.adjMax - section.adjMin)
                                #     # cv.drawContours(img, [PartMoved.getContour()], -1, (0, 0, int( 255 * (partSideId / vertexLength) ) ), 2, cv.LINE_8)
                                #     cv.circle(img, pointCheckNew, 2, (255, 0, 0), 2)
                                #     cv.circle(img, pointCheckNew, abs(int(distance)), (0, 0, 255), 1)

                                if sectionDistances[cutoutId] > distance:
                                    sectionDistances[cutoutId] = distance
                                # cv.circle(img, pointCheckNew, abs(int(distance)), (255, 0, 0), 1)
                                if distance < checkDistance:
                                    if distance < minDistance: minDistance = distance
                                    safePlace = False
                                    # if ( section.partOffId == 18 and ( partSideId == 5 or partSideId == 11 ) and (section.adjMax - section.adjMin) == 153 ): # and distance == 13.408956583091223
                                    #     print("###", distance, cutoutId, partSideCheckId, pointCheckNew, predistance, section.adjMax - section.adjMin)
                                    #     cv.circle(img, pointCheckNew, 1, (255, 0, 0), 1)
                                    #     cv.circle(img, pointCheckNew, abs(int(distance)), (0, 0, 255), 1)
                                    #     cv.drawContours(img, [PartMoved.getContour()], -1, (0, 0, int( 255 * (partSideId / vertexLength) ) ), 2, cv.LINE_8)
                                        # cv.line(img, PointCheckA, PointCheckB, (0, 255, 0), )
                                    break

                                remainingLength -= distance
                                if distance > remainingLength + checkDistance:
                                    checking = False

                        else:
                            if distance < minDistance: minDistance = distance
                            safePlace = False
                            # cv.drawContours(img, [PartMoved.getContour()], -1, (0, 0, int( 255 * (partSideId / vertexLength) ) ), 2, cv.LINE_8)

                            break
                            # cv.circle(img, pointCheck, abs(int(distance)), (0, 0, 255), 1)
                            print("Can't Fit", partSideCheckId, pointCheck, distance, CheckLength, CheckLength + checkDistance)

                        if safePlace == False: break
                    if safePlace == False: break
                
                # print(safePlace, minDistance, testingDistance)
                if safePlace == False: 
                    
                    if minDistance - checkDistance > -4:
                        testingDistance += 4
                    else:
                        testingDistance += -(minDistance - checkDistance)

                    continue
            
                
                    

                # print(PointA, (sectionAngle - PartSectionAngle + math.pi), PointARot, testPoint, sectionDistances)
                # if average([sectionDistances[i] for i in range(len(mat.cutouts))]) < 22:
                # displayImage(img)
                # print(PartMoved)
                # score = 1
                score = calculatePerimeter(mat, PartMoved, sectionDistances)
                # print(score)
                if ( partSideId == 5 or partSideId == 11 ):
                    cv.drawContours(img, [PartMoved.getContour()], -1, (0, 0, int( 255 * (partSideId / vertexLength) ) ), 2, cv.LINE_8)

                    
                if score > bestScore:
                    # print(sectionDistances)
                    calculatePerimeter(mat, PartMoved, sectionDistances, True)
                    bestScore = score
                    bestPartPlacement = PartMoved
                    bestInfo = (xMove, yMove, angleRotated)

                if score < bestScore * 0.5:
                    nearestDistance = mat.width
                    for i in range(len(mat.cutouts)):
                        if not i == section.partOffId:
                            nearestDistance = min(nearestDistance, sectionDistances[i])
                    testingDistance += max(4, nearestDistance - checkDistance)

                else:
                    nearestDistance = mat.width
                    for i in range(len(mat.cutouts)):
                        nearestDistance = min(nearestDistance, sectionDistances[i])
                    testingDistance += max(4, nearestDistance - checkDistance)
            






    if bestPartPlacement != None:
        cv.drawContours(img, [bestPartPlacement.getContour()], -1, (255, 0, 0), 5, cv.LINE_8)

    cv.imwrite("frontend/build/placementOutput/OutputImage.jpg", img)
    print(bestScore, bestInfo)

    # displayImage(img)




    return bestInfo