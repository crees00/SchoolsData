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
import dateutil.parser as parser
import matplotlib.pyplot as plt

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
        self.predecessorURNs = []  # list of URNs
        self.predecessors = []  # list of instances of School
        self.status = "closed"  # 'open' or 'closed'
        self.lastFirst = []  # all instances of inspection
        self.lastFirstCats = (
            []
        )  # [no of insps, ratings of most recent 4, avg of ones before]
        self.goods = []  # running total of goods from 1st inspection on
        self.bads = []

    def checkIfInspNoIsInList(self, inspNo):
        return inspNo in self.inspNosForSchool

    def __str__(self):
        return f"{self.getURN()} with {len(self.getInspections())} inspections: {[x.getCat() for x in self.getLastFirst()]}"

    def getURN(self):
        return self.URN

    def getPredecessors(self):
        return self.predecessors

    def getInspections(self):
        return self.inspections

    def getStatus(self):
        return self.status

    def getLastFirst(self):
        return self.lastFirst

    def getLastFirstCats(self):
        return self.lastFirstCats

    def getBads(self):
        return self.bads

    def getGoods(self):
        return self.goods

    def setStatus(self, statusIn):
        self.status = statusIn

    def setLastFirst(self, lastFirst):
        self.lastFirst = lastFirst

    def setLastFirstCats(self, lastFirstCats):
        self.lastFirstCats = lastFirstCats

    def setGoods(self, goods):
        self.goods = goods

    def setBads(self, bads):
        self.bads = bads

    def addInspToSchool(self, insp):
        ''' insp is an instance of Inspection '''
        if insp in self.getInspections():
            return
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
        # First check it isn't already in the list
        for existingPredecessor in self.getPredecessors():
            if existingPredecessor.getURN() == predURN:
                return
        global predsThatAreNotInDF
        try:
            self.predecessors.append(SchoolDict[predURN])
            self.predecessorURNs.append(predURN)
        except KeyError:
            predsThatAreNotInDF.append(predURN)


class Inspection:
    def __init__(self, inspNo, cat, URN, year):
        self.URN = URN
        self.cat = cat
        self.inspNo = inspNo
        self.year = year

    def __str__(self):
        return f"Inspection {self.getInspNo()}: Cat {self.getCat()}"

    def getURN(self):
        return self.URN

    def getCat(self):
        return self.cat

    def getInspNo(self):
        return self.inspNo

    def getYear(self):
        return self.year


def loadInspections(row):
    global inspList
    URN = int(row["URN"])
    date = row["Inspection start date"]
    inspNo = row["Inspection number"]
    if (type(inspNo) == str):
        if inspNo[:3] == 'ITS':
            inspNo = int(inspNo[3:])
    try:
        year = parser.parse(date).year
        currentInsp = Inspection(
            inspNo, row["Overall effectiveness"], URN, year
        )
    except TypeError:
        #        print(date, type(date),'did not parse')
        currentInsp = Inspection(
            inspNo, row["Overall effectiveness"], URN, 2004
        )
    # Generate an instance of Inspection for this row in df
    if currentInsp.getCat() in [1,2,3,4,9]:
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
            SchoolDict[insp.getURN()].addInspToSchool(insp)
            
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
    openAndUninspected = []
    if where in ["ONS", "Cdrive"]:
        file = "Data\edubaseallstatefunded20190704.csv"
    else:
        file = "edubaseallstatefunded20190627.csv"
    openSchools = pd.read_csv(sf.addFolderPath(file), encoding="latin-1")
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


def sortInspectionsToLastFirst(school):
    tupList, years, lastFirst, lastFirstCats = [], [], [], []
    for insp in school.inspections:
        tupList.append((insp, insp.getYear()))
        years.append(insp.getYear())
    years.sort(reverse=True)
    for year in set(years):
        for tup in tupList:
            if tup[1] == year:
                lastFirst.append(tup[0])
                lastFirstCats.append(tup[0].getCat())
    # Put the average of all previous inspections
    if len(tupList) > 4:
        avg = np.mean(lastFirstCats[4:])
        lastFirstCats = lastFirstCats[:4]
        lastFirstCats.append(avg)
    # If exactly 4 inspections, put the average as the 4th inspection
    elif len(tupList) == 4:
        lastFirstCats.append(lastFirstCats[3])
    lastFirstCats.insert(0, len(tupList))
    school.setLastFirst(lastFirst)
    school.setLastFirstCats(lastFirstCats)
    return school


def feedToSort(SchoolDict):
    for URN in SchoolDict.keys():
        SchoolDict[URN] = sortInspectionsToLastFirst(SchoolDict[URN])
    return SchoolDict


def clusterDF(SchoolDict, write=""):
    df = pd.DataFrame()

    for URN in SchoolDict.keys():
        lastFirstCats = SchoolDict[URN].getLastFirstCats()
        if len(lastFirstCats) == 6:
            df[URN] = lastFirstCats
    if write != "":
        df.to_csv(write)
    return df


def makeURNvsYearInspCats(SchoolDict, write=""):
    URNdict = {}
    for URN in SchoolDict:
        school = SchoolDict[URN]
        if school.getStatus() == "closed":
            continue
        insps = school.getInspections()
        yearDict = {year: 0 for year in list(range(2005, 2019))}

        for insp in insps:
            flag = False
            year = insp.getYear()
            while flag == False:
                if yearDict[year] == 0:
                    yearDict[year] = insp.getCat()
                    flag = True
                elif year > 2005:
                    year -= 1
                #                    print(SchoolDict[URN])
                else:
                    flag = True
        URNdict[URN] = yearDict

    dfOut = pd.DataFrame(URNdict)
    if write != "":
        dfOut.to_csv(write)
    return dfOut


def makeGoodsAndBadsLists(SchoolDict):
    """ Makes lists in time (non-reversed) order i.e. starts at 1st insp"""
    for URN in SchoolDict:
        school = SchoolDict[URN]
        goods, bads, current = [], [], [0, 0]
        for insp in reversed(school.getLastFirst()):
            if insp.getCat() in [1, 2]:
                current[0] += 1
            elif insp.getCat() in [3, 4]:
                current[1] += 1
            goods.append(current[0])
            bads.append(current[1])
        school.setGoods(goods)
        school.setBads(bads)
    return SchoolDict


def plotGvsB(SchoolDict):
    a = 0
    for URN in SchoolDict:
        goods = SchoolDict[URN].getGoods()
        bads = SchoolDict[URN].getBads()
        if len(goods) == 0:
            goods, bads = [0], [0]
        plt.scatter(goods[-1], bads[-1], color="k", alpha=(1 / 255))
        a += 1
        if a > 1000:
            break


def makeMatrices(SchoolDict):
    finalPt = np.zeros((10,10))  # bads, goods
    steps = np.zeros((10,10))
    maxgoods=0
    maxbads=0
    for URN in SchoolDict:
        if SchoolDict[URN].getStatus() == 'closed':
            continue
        goods = SchoolDict[URN].getGoods()
        bads = SchoolDict[URN].getBads()
        if len(goods)>maxgoods:
            if URN != 135886:
                maxgoods = len(goods)
                goodURN = URN
        if len(bads)>maxbads:
            maxbads = len(bads)
            badURN = URN
        if len(goods) == 0:
            goods, bads = [0], [0]
        finalPt[bads[-1], goods[-1]] += 1
        for i in range(len(goods)):
            steps[bads[i], goods[i]] += 1
        steps[0, 0] = len(SchoolDict)
    print('goods:',maxgoods, goodURN)
    print('bads:',maxbads, badURN)
    return finalPt, steps


def findOpenSchools(SchoolDict):
    import copy

    outDict = {}
    for URN in SchoolDict.keys():
        if SchoolDict[URN].getStatus() == "open":
            outDict[URN] = copy.copy(SchoolDict[URN])
    return outDict


def findGrandParents(SchoolDict, printout=False):
    threeGenerations = []
    for school in SchoolDict.values():
        if school.getStatus() =='open':
            for predecessor in school.getPredecessors():
                if len(predecessor.getPredecessors()) > 0:
                    threeGenerations.append(
                        (school, predecessor, predecessor.getPredecessors())
                    )
    if printout:
        for (ch, par, gp) in threeGenerations:
            print("child:\n", ch.getURN())
            print("parent:\n", par.getURN())
            print("grandparent(s):\n", {x.getURN() for x in gp})
            print()
    return threeGenerations




def grouping(openSchoolDict, printout=False):
    groupDict = {
        x: [] for x in ["stuck", "becomeStuck", "becomingStuck", "escaped", "downUp"]
    }
    print("making groups")
    groupDict["stuck"] = filterSchools(
        openSchoolDict.values(), numMin=4, cats=[[3, 4]] * 15
    )
    for ones in range(4, 7):
        groupDict["becomeStuck"] += filterSchools(
            openSchoolDict.values(), cats=[[3, 4]] * ones + [[1, 2]]
        )
    for ones in range(1, 4):
        groupDict["becomingStuck"] += filterSchools(
            openSchoolDict.values(), cats=[[3, 4]] * ones + [[1, 2]]
        )
    for ones in range(1, 5):
        groupDict["escaped"] += filterSchools(
            openSchoolDict.values(), cats=[[1, 2]] * ones + [[3, 4]] * 4
        )
    for ones in range(1, 5):
        for twos in range(1, 5):
            for threes in range(1, 5):
                groupDict["downUp"] += filterSchools(
                    openSchoolDict.values(),
                    cats=[[1, 2]] * ones + [[3, 4]] * twos + [[1, 2]] * threes,
                )
    if printout:
        import itertools

        for group in groupDict.keys():
            print(f"{group} has {len(groupDict[group])} items")
        print("checking if there is any crossover between groups...")
        for (group, otherGroup) in itertools.combinations(groupDict.keys(), 2):
            if (group != otherGroup) and (
                len(set(groupDict[group]) & set(groupDict[otherGroup])) > 0
            ):
                print(
                    group,
                    "and",
                    otherGroup,
                    "share",
                    len(set(groupDict[group]) & set(groupDict[otherGroup])),
                    "items",
                )
    return groupDict


def runAll():
    global predsThatAreNotInDF
    predsThatAreNotInDF = []
    global inspList
    global SchoolDict
    inspList = []
    df = pd.read_csv(sf.addFolderPath("bigDFnoDups1.csv"))
    df = df.apply(loadInspections, axis=1)
    SchoolDict, allInspNos, dupInsps = assignInspectionsToSchools(inspList)
    df = df.apply(addPredecessorURNsFromDF, axis=1)
    SchoolDict = addAllPredecessors(SchoolDict)
    stuck = calcStuck(SchoolDict)
    SchoolDict, openAndUninspected = setAllStatuses(SchoolDict)
    openStuck = whichStuckAreOpen(stuck)
    SchoolDict = feedToSort(SchoolDict)
    dfForClustering = clusterDF(SchoolDict,sf.addFolderPath("clusterDF.csv"))
    SchoolDict = makeGoodsAndBadsLists(SchoolDict)
    dfOut = makeURNvsYearInspCats(SchoolDict, sf.addFolderPath("dfOut.csv"))
#    finalPt, steps = makeMatrices(SchoolDict)
    openSchoolDict = findOpenSchools(SchoolDict)
    threeGenerations = findGrandParents(SchoolDict)
#    groupDict = grouping(openSchoolDict)
    groupDict={}
    return SchoolDict, openSchoolDict, groupDict

if __name__ == "__main__":
    SchoolDict, openSchoolDict, groupDict = runAll()
#groupDict = grouping(openSchoolDict, True)

print(f"took {datetime.datetime.now()-start}")
