from util.Material import Material
from util.Cutout import Cutout
from util.methods.MatFromImage import GenerateMaterial
from util.CustomMath import getAngle, getLength
import cv2 as cv
import numpy as np
import math

material = GenerateMaterial('Real-01.jpg')
# print(material.findSections(20))



material.print()

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