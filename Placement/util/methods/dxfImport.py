from Placement.util.Part import Part
import ezdxf
from ezdxf.entities.spline import Spline

class DxfObject:

    def __init__(self, startPoint, endPoint, objectData, inverted = False) -> Part:
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.objectData = objectData
        self.inverted = inverted

    def toggleInverted(self):
        self.inverted = not self.inverted
        temp = self.startPoint
        self.startPoint = self.endPoint
        self.endPoint = temp

def partFromDxf(filePath) -> Part:

    # Load File
    try:
        doc = ezdxf.readfile(filePath)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        return 0
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        return 0

    # Get ModelSpace
    msp = doc.modelspace()

    loops = []

    #function to add loop to each loop chain 
    def addLoop(startPoint, endPoint, objectData):
        if len(loops) == 0:
            loops.append([
                DxfObject(startPoint, endPoint, objectData)
            ])
            return True
        foundLoop = False
        for i in range(len(loops)):
            # print(loops[i][-1].endPoint, startPoint)
            if loops[i][-1].endPoint == startPoint:
                loops[i].append(DxfObject(startPoint, endPoint, objectData))
                foundLoop = True
                break
            elif loops[i][-1].endPoint == endPoint:
                loops[i].append(DxfObject(endPoint, startPoint, objectData, True))
                foundLoop = True
                break

        if foundLoop == False:
            loops.append([
                DxfObject(startPoint, endPoint, objectData)
            ])


    def detectElement(e):
        # print(e)

        if e.dxftype() == 'LWPOLYLINE':

            for element in e.virtual_entities():
                detectElement(element)

        elif e.dxftype() == 'LINE':
            addLoop(e.dxf.start, e.dxf.end, e)

        elif e.dxftype() == 'SPLINE':
            addLoop(e.control_points[0], e.control_points[-1], e)

        elif e.dxftype() == 'ARC':
            addLoop(e.start_point, e.end_point, e)

        else:
            print(f"AP: DXF Insert Error. DXF element type {e.dxftype()} not supported")
            return "Error"

    # Loop through dxf Elements and addloops to join together
    for i in range(len(msp)):
        # print(i, len(msp))
        e = msp[i]
        i += 1

        # print(e)

        response = detectElement(e)
        # print(response)
        if response == "Error":
            return None
        if response == None:
            pass      

    #join loops
    changed = True
    while changed == True:
        changed = False
        currentChain = len(loops) - 1
        while currentChain >= 0:
            for i in range(len(loops)):
                # print(i, currentChain, len(loops))
                if i == currentChain:
                    continue

                if loops[i][-1].endPoint == loops[currentChain][0].startPoint:
                    loops[i].extend(loops[currentChain])
                    loops.pop(currentChain)
                    changed = True
                    break
                if loops[i][-1].endPoint == loops[currentChain][-1].endPoint:
                    newArray = []
                    for element in reversed(loops[currentChain]):
                        element.toggleInverted()
                        newArray.append(element)
                    loops[i].extend(newArray)
                    loops.pop(currentChain)
                    changed = True
                    break

            currentChain -= 1

    parts = []
    greatestIndex = None
    greatestArea = 0
    for i in range(len(loops)):
        loop = loops[i]
        
        if loop[0].startPoint != loop[-1].endPoint: continue

        parts.append(Part()) # Setup part object for points to be put into

        for elementId in range(len(loop)):
            element = loop[elementId]
            e = element.objectData

            # print(element.startPoint, element.endPoint, element.objectData.dxftype(), element.inverted)

            if e.dxftype() == 'LINE':

                if not element.inverted:
                    parts[i].addPoint(e.dxf.start)
                    parts[i].addPoint(e.dxf.end)
                else:
                    parts[i].addPoint(e.dxf.end)
                    parts[i].addPoint(e.dxf.start)

            elif e.dxftype() == 'SPLINE':
                if not element.inverted:
                    for point in e.control_points:
                        parts[i].addPoint(point)
                else:
                    for point in reversed(e.control_points):
                        parts[i].addPoint(point)
                        
            elif e.dxftype() == 'ARC':
                if not element.inverted:
                    for point in e.flattening(1):
                        parts[i].addPoint(point)
                else:
                    for point in reversed(e.flattening(1)):
                        parts[i].addPoint(point)

            if (elementId != len(loop) -1):    
                parts[i].vertices.pop()
                        
        
        parts[i].vertices.pop()
        parts[i].transformToContour() # Rearrange points so that they are all positive

        area = parts[i].findArea()

        if greatestArea < area:
            greatestArea = area
            greatestIndex = i
    
    return parts[greatestIndex]