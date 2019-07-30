# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 19:21:12 2019

@author: reesc1
"""


class Node:
    def __init__(self, schoolsIn, patternIn):
        self.schoolsIn = schoolsIn  # list of instances of School
        self.patternIn = patternIn  # 'gbg'
        self.schoolsOutG = []  # list of instances of School
        self.schoolsOutB = []
        self.schoolsStayingHere = []
        self.uncategorised = []
        self.findGOutSchools()
        if len(self.getSchoolsStaying()) < len(self.getSchoolsIn()):
            nodeDict[self.getPatternIn() + "g"] = Node(
                self.getSchoolsOutG(), self.getPatternIn() + "g"
            )
            nodeDict[self.getPatternIn() + "b"] = Node(
                self.getSchoolsOutB(), self.getPatternIn() + "b"
            )

    def __str__(self):
        return f"\n{self.getPatternIn()} - In: {len(self.getSchoolsIn())} - Staying: {len(self.getSchoolsStaying())}\nGood: {len(self.getSchoolsOutG())}, Bad: {len(self.getSchoolsOutB())}"

    def getSchoolsIn(self):
        return self.schoolsIn

    def getPatternIn(self):
        return self.patternIn

    def addSchoolToStayingHere(self, school):
        self.schoolsStayingHere.append(school)

    def addSchoolToOutG(self, school):
        self.schoolsOutG.append(school)

    def addSchoolToOutB(self, school):
        self.schoolsOutB.append(school)

    def getSchoolsStaying(self):
        return self.schoolsStayingHere

    def getSchoolsOutG(self):
        return self.schoolsOutG

    def getSchoolsOutB(self):
        return self.schoolsOutB

    def findGOutSchools(self):
        schoolsIn = self.getSchoolsIn()
        pattern = self.getPatternIn()
        for school in schoolsIn:
            lastFirst = school.getLastFirst()  # list of instances of Inspection
            if len(lastFirst) == len(pattern):
                self.addSchoolToStayingHere(school)
                continue
            insp = lastFirst[len(pattern) - 1]
            if insp.getCat() in [1, 2]:
                self.addSchoolToOutG(school)
                continue
            elif insp.getCat() in [3, 4]:
                self.addSchoolToOutB(school)
                continue
            else:
                self.uncategorised.append(school)


nodeDict = {}
nodeDict["0"] = Node([x for x in SchoolDict.values()], "")

# node0 =
# node1G = Node(node0.getSchoolsOutG(),'g')
# node1B = Node(node0.getSchoolsOutB(),'b')
#


def printNodeDict(nodeDict, layers=4):

    #    for layer in range(layers):
    width = ((2 ** layers) * 4) # Whole width
    centrePt = (width // 2) + 1
    nodeLabel = ""
    # Layer0
    strings = []
    strings.append(
        "," * (centrePt - 1) + str(nodeDict["0"].getPatternIn()) + "," * (centrePt - 1)
    )
    strings.append(
        "," * (centrePt - 1)
        + str(len(nodeDict["0"].getSchoolsIn()))
        + "," * (centrePt - 1)
    )
    strings.append("," * (centrePt - 2) + "G,S,B" + "," * (centrePt - 2))
    strings.append(
        "," * (centrePt - 2)
        + str(len(nodeDict["0"].getSchoolsOutG()))
        + ","
        + str(len(nodeDict["0"].getSchoolsStaying()))
        + ","
        + str(len(nodeDict["0"].getSchoolsOutB()))
        + "," * (centrePt - 2)
    )
    strings.append('')
    
    nodeLabels = ['g','b']
    lines = {}
    for nodeLabel in nodeLabels:
        lines[nodeLabel] =  makeOneNode(nodeDict, nodeLabel)
    for nodeLabel in nodeLabels:
        centrePt = width // ((len(nodeLabel)+1) * 2)
        spacer = (centrePt-2) * ','
        
    
    
    
    with open("classTree.csv", "w") as f:
        for line in strings:
            f.write(line)
            f.write("\n")

def makeAllNodes(nodeDict):
    treeDict = {}
    for nodeLabel in nodeDict.keys():
        strings = []
        
        strings.append(
            ','+str(nodeDict[nodeLabel].getPatternIn()) + ','
        )
        strings.append(
             ','+str(len(nodeDict[nodeLabel].getSchoolsIn()))+','
        )
        strings.append( "G,S,B" )
        strings.append(
             str(len(nodeDict[nodeLabel].getSchoolsOutG()))
            + ","
            + str(len(nodeDict[nodeLabel].getSchoolsStaying()))
            + ","
            + str(len(nodeDict[nodeLabel].getSchoolsOutB()))
        )
        strings.append('')
        treeDict[nodeLabel] = strings
    return treeDict

    
def buildLayerOfNodes(treeDict, layer, totalLayers):
    numNodes = 2**layer
    width =((2 ** totalLayers) * 6)+1 # Whole width
    print('\nlayer',layer)
    print('width',width)
    spacing = (width - (numNodes*3))//(numNodes)
    print('spacing',spacing)
    if spacing < 2:
        spacing = 2
    lines = [','*(spacing//2)] * 5
    spaceUsed = len(lines)
    nodesLeftInLayer = numNodes
    for sequence in itertools.product('gb', repeat = layer):
        nodeLabel = ''
        spacing = (width-(len(lines[0]) + nodesLeftInLayer*3)) // (nodesLeftInLayer+1)
        if spacing < 2:
            spacing = 2

        if layer >2:
            print(nodesLeftInLayer,len(lines[0]),(width-(len(lines[0])+nodesLeftInLayer*3)),spacing)
        for item in sequence:
            nodeLabel += item
#        print(nodeLabel)
#        print(lines)
        for i,line in enumerate(lines):
#            print(treeDict[nodeLabel][i])
            if nodeLabel == '':
                lines[i] += treeDict['0'][i]
            else:
                try:
                    lines[i] += treeDict[nodeLabel][i]
                except KeyError:
                    lines[i] += ','*3
            lines[i] += ','*spacing
        nodesLeftInLayer -= 1
#            print(line)
#            print(lines)
    return lines            
  
def makeWholeTree(nodeDict):
    treeDict = makeAllNodes(nodeDict)
    totalLayers =5#  max([len(x) for x in nodeDict.keys()])
    lines = []
    with open("classTree.csv", "w") as f:
        for layer in range(totalLayers+1):
            for line in buildLayerOfNodes(treeDict, layer, totalLayers):
                f.write(line)
                f.write("\n")

makeWholeTree(nodeDict)  
#printNodeDict(nodeDict)
