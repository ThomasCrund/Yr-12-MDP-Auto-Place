from Placement.util.Part import Part
import ezdxf
from ezdxf.entities.spline import Spline

class DxfObject:

    def __init__(self, startPoint, endPoint, objectData, inverted = False):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.objectData = objectData
        self.inverted = inverted

    def toggleInverted(self):
        self.inverted = not self.inverted
        temp = self.startPoint
        self.startPoint = self.endPoint
        self.endPoint = temp

def partFromDxf(filePath):

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
        # print(e, msp[1])


        if e.dxftype() == 'LWPOLYLINE':
            for element in e.virtual_entities():
                # print(element)
                detectElement(element)
            pass
        elif e.dxftype() == 'LINE':
            # print(e.dxf.start, e.dxf.end, e.dxf.layer)
            addLoop(e.dxf.start, e.dxf.end, e)
        elif e.dxftype() == 'SPLINE':
            # print(e.control_points[0], e.control_points[-1])
            addLoop(e.control_points[0], e.control_points[-1], e)
            # for point in e.control_points:
            #     print(point)
        elif e.dxftype() == 'ARC':
            detectElement(Spline.from_arc(e))

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

                # 
                # I have left what could be a possible error if the entire chain is the wrong way around
                # I don't know if this can occur so I have code to print if it is detected as happening (I can't test/ fix if i don't know how to create)
                # 
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

    # invertedCatch = False
    # print(len(loops))
    for i in range(len(loops)):
        loop = loops[i]
        print(f"loop {i}")
        for element in loop:
            # if element.inverted == True:
            #     invertedCatch = True
            print(element.startPoint, element.endPoint, element.objectData.dxftype(), element.inverted)

    
    # if invertedCatch:
    #     print("### An element DXF is inverted this could cause errors check to ensure correctly working")

    return Part()