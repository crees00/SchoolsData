# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:38:24 2019

@author: reesc1
"""
import pandas as pd
import numpy as np
import datetime
import re
import setFolder as sf

where = sf.where
start = datetime.datetime.now()
print(f"starting at {start}")


class School:
    def __init__(self, URN):
        self.URN = URN
        #        self.inspDict = {1: [], 2: [], 3: [], 4: [], 9: []}
        self.ones, self.twos, self.threes, self.fours, self.nines = [], [], [], [], []
        self.inspNosForSchool = []
        self.inspections = []  # list of instances of Inspection
        self.predecessorURNs = []
        self.predecessors = []
        self.status = "closed"  # 'open' or 'closed'

    def checkIfInspNoIsInList(self, inspNo):
        return inspNo in self.inspNosForSchool

    def __str__(self):
        return f"{self.getURN()} with {len(self.getInspections())} inspections: {[x.getCat() for x in self.getInspections()]}"

    def getURN(self):
        return self.URN

    def getPredecessors(self):
        return self.predecessors

    def getInspections(self):
        return self.inspections

    def getStatus(self):
        return self.status

    def setStatus(self, statusIn):
        self.status = statusIn

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

    def addPredecessorFromURN(self, predURN):
        try:
            self.predecessors.append(SchoolDict[predURN])
            self.predecessorURNs.append(predURN)
        except KeyError:
            predsThatAreNotInDF.append(predURN)


class Inspection:
    def __init__(self, inspNo, cat, URN):
        self.URN = URN
        #        self.date = date
        self.cat = cat
        self.inspNo = inspNo

    def __str__(self):
        return f"Inspection {self.getInspNo()}: Cat {self.getCat()}"

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
        row["Inspection number"], row["Overall effectiveness"], URN
    )
    inspList.append(currentInsp)
    return row


def assignInspectionsToSchools(inspList):
    SchoolDict = {}
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
    print("inspections assigned to schools")
    return SchoolDict, allInspNos, dupInsps


def addPredecessorURNsFromDF(row):
    global SchoolDict
    pred = row["Predecessor School URN(s)"]
    URN = int(row["URN"])
    predList = re.findall("[0-9]{4,7}", str(pred))
    if len(predList) > 0:
        for no in predList:
            no = int(no)
            # Check current URN isn't listed as a predecessor
            if no == row["URN"]:
                continue
            try:
                SchoolDict[URN].addPredecessorFromURN(no)
            except KeyError:
                SchoolDict[URN] = School(URN)
                SchoolDict[URN].addPredecessorFromURN(no)
    return row


def addPredecessorInspections(school):
    for pred in school.getPredecessors():
        if len(pred.getPredecessors()) > 0:
            pred = addPredecessorInspections(pred)
        for insp in pred.getInspections():
            if school.checkIfInspNoIsInList(insp.getInspNo()) == False:
                school.addInspToSchool(insp)
    return school


def addAllPredecessors(SchoolDict):
    for URN in SchoolDict.keys():
        SchoolDict[URN] = addPredecessorInspections(SchoolDict[URN])
    print("all predecessors added")
    return SchoolDict


def calcStuck(SchoolDict):
    stuck = []
    for URN in SchoolDict.keys():
        tally = []
        flag = False
        for insp in SchoolDict[URN].getInspections():
            cat = insp.getCat()
            if (cat == 1) or (cat == 2):
                flag = True
                break
            tally.append(cat)
        if (len(tally) >= 4) and (not flag):
            stuck.append(SchoolDict[URN])
    print("stuck schools found")
    return stuck


def setAllStatuses(SchoolDict):
    folderPath = sf.folderPath
    openAndUninspected = []
    if where == "ONS":
        file = "Data\edubaseallstatefunded20190704.csv"
    else:
        file = "edubaseallstatefunded20190627.csv"
    openSchools = pd.read_csv(folderPath + file, encoding="latin-1")
    openSchoolsSet = set(openSchools["URN"])
    for URN in openSchoolsSet:
        try:
            SchoolDict[URN].setStatus("open")
        except KeyError:
            SchoolDict[URN] = School(URN)
            SchoolDict[URN].setStatus("open")
            openAndUninspected.append(SchoolDict[URN])
    print("school statuses set")
    return SchoolDict, openAndUninspected


def whichStuckAreOpen(stuck):
    openStuck = []
    for school in stuck:
        if school.getStatus() == "open":
            openStuck.append(school)
    print(f"{len(openStuck)} open stuck schools")
    return openStuck


predsThatAreNotInDF = []
inspList = []
df = pd.read_csv("bigDFnoDups1.csv")

df = df.apply(loadInspections, axis=1)
SchoolDict, allInspNos, dupInsps = assignInspectionsToSchools(inspList)
df = df.apply(addPredecessorURNsFromDF, axis=1)
SchoolDict = addAllPredecessors(SchoolDict)
stuck = calcStuck(SchoolDict)
SchoolDict, openAndUninspected = setAllStatuses(SchoolDict)
openStuck = whichStuckAreOpen(stuck)
print(f"took {datetime.datetime.now()-start}")
