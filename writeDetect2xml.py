import os
import math
import numpy as np
import xml.etree.ElementTree as ET

information = {"name":"",
               "pose":u"Unspecified",
               "truncated":'0',
               "difficult":'0',
               "bndbox":{"xmin":0,
                          "ymin":0,
                          "xmax":0,
                          "ymax":0}}

classes = ['Vehicle', 'Person', 'Bike', 'aa', 'aa']

def findDetectTxt(xmlName, txtDir):
    frameID = int(xmlName.split('.')[0])
    temp = frameID
    if temp % 3 != 1:
        for ii in range(1, 3):
            frameID = temp - ii
            if frameID % 3 != 1:
                continue
            else:
                break
    nameString = '%06d.txt'
    txtName = nameString % frameID
    txtPath = os.path.join(txtDir, txtName)
    return txtPath

def indent(elem, level=0):
    #you are beautiful
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def generateElement(boundingBox):
    #generate element of object by boundingBox
    fatherNode = ET.Element("object")
    for k,v in information.items():
        child = ET.Element(k)
        fatherNode.append(child)
        if k == "name":
            child.text = classes[int(boundingBox[-1])]
        elif k == "bndbox":
            for k1,v1 in information["bndbox"].items():
                child0 = ET.Element(k1)
                child.append(child0)
                if k1 == "xmin":
                    child0.text = str(math.floor(boundingBox[0]))
                elif k1 == "ymin":
                    child0.text = str(math.floor(boundingBox[1]))
                elif k1 == "xmax":
                    child0.text = str(math.floor(boundingBox[2]))
                else:
                    child0.text = str(math.floor(boundingBox[3]))
        else:
            child.text = v

    return fatherNode

if __name__ == "__main__":
    xmlDir = r'F:\labelWithMask-RCNN\VIRAT_S_000201_08_001652_001838'
    txtDir = r'F:\labelWithMask-RCNN\VIRAT_S_000201_08_001652_001838_txt'
    xmlNames = os.listdir(xmlDir)
    for xmlName in xmlNames:
        xmlPath = os.path.join(xmlDir, xmlName)
        tree = ET.parse(xmlPath)
        fatherNode = tree.getroot()
        txtPath = findDetectTxt(xmlName, txtDir)
        boundingBoxes = np.loadtxt(txtPath)
        if len(boundingBoxes.shape) > 1:
            for boundingBox in boundingBoxes:
                node = generateElement(boundingBox)
                fatherNode.append(node)
            indent(fatherNode, 0)
            tree.write(xmlPath)
        else:
            boundingBox = boundingBoxes
            node = generateElement(boundingBox)
            fatherNode.append(node)
            indent(fatherNode, 0)
            tree.write(xmlPath)
