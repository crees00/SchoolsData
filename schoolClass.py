# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:38:24 2019

@author: reesc1
"""
import pandas as pd
import numpy as np
import datetime
import re

start = datetime.datetime.now()
print(f'starting at {start}')

class School:
    def __init__(self, URN):
        self.URN = URN
#        self.inspDict = {1: [], 2: [], 3: [], 4: [], 9: []}
        self.ones,self.twos,self.threes,self.fours,self.nines = [],[],[],[],[]
        self.inspNosForSchool = []
        self.inspections = [] # list of instances of Inspection
        self.predecessorURNs = []
        self.predecessors = []
        
    def checkIfInspNoIsInList(self,inspNo):
        return inspNo in self.inspNosForSchool            
        
    
    def getURN(self):
        return self.URN
    
    def getPredecessors(self):
        return self.predecessors
    
    def getInspections(self):
        return self.inspections
    
    def addInspToSchool(self, insp):
        self.inspections.append(insp)
        self.inspNosForSchool.append(insp.getInspNo())
        if insp.getCat() == 1:
            self.ones.append(insp)
        elif insp.getCat() == 2:
            self.twos.append(insp)
        elif insp.getCat() == 3:
            self.threes.append(insp)
        elif insp.getCat() == 4:
            self.fours.append(insp)
        else:
            self.nines.append(insp)
    
    def addPredecessorURNs(self, predURN):
        self.predecessorURNs.append(predURN)
        try:
            self.predecessors.append(SchoolDict[predURN])
        except KeyError:
            predsThatAreNotInDF.append(predURN)
        
class Inspection:
    def __init__(self, inspNo, cat, URN):
        self.URN = URN
        #        self.date = date
        self.cat = cat
        self.inspNo = inspNo

    def getURN(self):
        return self.URN

    def getCat(self):
        return self.cat

    def getInspNo(self):
        return self.inspNo


def loadInspections(row):
    global inspList
    URN = int(row["URN"])
    # Generate an instance of Inspection for this row in df
    currentInsp = Inspection(
            row["Inspection number"], row["Overall effectiveness"],URN 
        )
    inspList.append(currentInsp)
    return row

def assignInspectionsToSchools(inspList):
    SchoolDict={}              
    allInspNos = [] 
    dupInsps = []      
    for insp in inspList:
        # check inspection no not added already
        if insp.getInspNo() in allInspNos:
            dupInsps.append(insp)
            continue
        # add inspection number to list of inspections
        allInspNos.append(insp.getInspNo())
        try:
            SchoolDict[insp.getURN()].addInspToSchool(insp)
        except KeyError:
            SchoolDict[insp.getURN()] = School(insp.getURN()) 
            
    return SchoolDict, allInspNos, dupInsps    



def addPredecessorURNs(row):
    global SchoolDict
    pred = row["Predecessor School URN(s)"]
    URN = int(row['URN'])
    predList = re.findall("[0-9]{4,7}", str(pred))
    if len(predList) > 0:
        for no in predList:
            no = int(no)
            # Check current URN isn't listed as a predecessor
            if no == row["URN"]:
                continue
            try:
                SchoolDict[URN].addPredecessor(no)
            except KeyError:
                SchoolDict[URN] =School(URN)
                SchoolDict[URN].addPredecessor(no)
    return row

def addPredecessorInspections(school, SchoolDict):
    for URN in school.getPredecessors():
        if len(SchoolDict[URN].getPredecessors())>0:
            addPredecessorInspections(SchoolDict[URN])
        for insp in SchoolDict[URN].getInspections:
            if school.checkIfInspNoIsInList(inspNo) == False:
                school.addInspToSchool(insp)
    return school

def addAllPredecessors(SchoolDict):
    for URN in SchoolDict.keys():
        SchoolDict[URN] = addPredecessorInspections(SchoolDict[URN], SchoolDict)
    return SchoolDict

predsThatAreNotInDF = []
inspList = []
df = pd.read_csv("bigDFnoDups1.csv")
#
df = df.apply(loadInspections, axis=1)
SchoolDict, allInspNos, dupInsps = assignInspectionsToSchools(inspList)
df = df.apply(addPredecessorURNs, axis=1)
SchoolDict = addAllPredecessors(SchoolDict)
    

print(f'took {datetime.datetime.now()-start}')