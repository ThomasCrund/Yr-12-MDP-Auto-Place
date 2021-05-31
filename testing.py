from Placement.util.Material import Material
from Placement.util.Cutout import Cutout
from Placement.util.methods.MatFromImage import GenerateMaterial
from Placement.util.methods.dxfImport import partFromDxf
from Placement.util.methods.place import placePerimeter
from Placement.util.methods.ImageOutput import generateImg, displayImage
from Placement.util.CustomMath import getAngle, getLength, rotateAroundPoint
import cv2 as cv
import numpy as np
import math
import time

# print("Test")
# partFromDxf("TestFiles/TestDXF.dxf")
# partFromDxf("TestFiles/TestDXFCutout.dxf")

# Generate Material
material = GenerateMaterial('Placement/TestAngleHard.jpg')
# material = GenerateMaterial('Placement/Real-01.jpg')

material.print()

# part.print()
# part.rotate((0, 0), math.pi/4).print()

# Calculate the best position for the part

# # Import DXF into part
# part = partFromDxf("TestFiles/Large.dxf")


# startTime = time.time()


# placePerimeter(material, part);

# print(time.time() - startTime)



# print(material.cutouts[0].points)
# print(cv.contourArea(material.cutouts[0].points))
# material.print()




# img = np.ones((material.height, material.width, 3), np.uint8)*255
# for pointId in range(len(material.cutouts[8].points)):
#     pointX, pointY = material.cutouts[8].points[pointId][0]
#     print(pointX, pointY, pointId * 3)
#     color = (pointId * 3, 0,0)
#     # img[pointY][pointX] = color
#     cv.putText(img, str(pointId), (pointX , pointY - 5), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
#     cv.circle(img, (pointX, pointY), 5, color)

    # cv.drawContours(img, [cutout.getPoints()], -1, color, 2, cv.LINE_8)

# cv.imwrite('OutputImageTest.jpg', img)
# cv.imshow('Material Print', img)
# cv.waitKey(0)
# cv.destroyAllWindows()
# print(material.cutouts[8].points)


# img = np.ones((material.height, material.width, 3), np.uint8)*255


# cv.imshow('Side Points', img)
# cv.waitKey(0)
# cv.destroyAllWindows()