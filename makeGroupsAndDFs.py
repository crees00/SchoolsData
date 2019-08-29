# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 12:07:55 2019

Make df to use with genericModelClass

@author: reesc1
"""
import pandas as pd

def filterSchools(SchoolsList, numMin=0, numMax=20, cats=[[]] * 20, printout=False):
    """ Takes in list of schools, returns a list of schools which is a subset
    of the original. If no filters applied, returns original list.
    To only include cat 1&2 for 2nd most recent inspection:
        numMin = 2, cats = [[],[1,2]]"""
    if (numMin == 0) and (len(cats) < 20):
        numMin = len(cats)
        if printout:
            print(f"Setting numMin to {numMin}")
    numInsps = list(range(numMin, numMax))
    outList = []
    for school in SchoolsList:
        # set 'out' as true, and only change it to False if school breaks
        # a filter rule
        out = True
        lastFirst = [insp.getCat() for insp in school.getLastFirst()]  # List of cats
        if len(lastFirst) in numInsps:
            for i, insp in enumerate(cats):
                # if a filter is set
                if len(insp) > 0:
                    # if there are enough inspections for filter to apply
                    if len(lastFirst) > i:
                        # if the cat of this inspection is allowed by set filter
                        if lastFirst[i] not in insp:
                            out = False
        else:
            out = False
        if out:
            outList.append(school)
    if printout:
        print(f"{len(outList)} schools in cat {cats}")
    return outList

def newGrouping(openSchoolDict, printout=False):
    ''' returns a dictionary of lists
    i.e. {'xbb':[school1, school2,...],...}'''
    groupDict = {
        x: [] for x in ["xbb", "xbbb", "bbb", "gbb", "gbbb", "bbbb","stuck","all",'gsbbs','gsbbbs']
    }
    print("making groups")
    groupDict["xbb"] = filterSchools(
        openSchoolDict.values(), numMin=3, cats=[[]] + [[3, 4]] * 2
    )
    groupDict["xbbb"] += filterSchools(
            openSchoolDict.values(), cats=[[]] + [[3, 4]] * 3
        )
    groupDict["bbb"] += filterSchools(
            openSchoolDict.values(), cats= [[3, 4]] * 3
        )
    groupDict["gbb"] += filterSchools(
            openSchoolDict.values(), cats=[[1,2]] + [[3, 4]] * 2
        )
    groupDict["gbbb"] += filterSchools(
            openSchoolDict.values(), cats=[[1,2]] + [[3, 4]] * 3
        )
    groupDict["bbbb"] += filterSchools(
            openSchoolDict.values(), cats= [[3, 4]] * 4
        )
    groupDict["stuck"] += filterSchools(
            openSchoolDict.values(), numMin=4, cats= [[3, 4]] * 15
        )
    groupDict['all'] += filterSchools(
            openSchoolDict.values())
    for ones in range(1,8):
        for twos in range(2,5):
            groupDict["gsbbs"] += filterSchools(
            openSchoolDict.values(), cats= [[1,2]] * ones + [[3, 4]] * twos
        )
    for ones in range(1,8):
        for twos in range(3,8):
            groupDict["gsbbbs"] += filterSchools(
            openSchoolDict.values(), cats= [[1,2]] * ones + [[3, 4]] * twos
        )

    if printout:
        import itertools

        for group in groupDict.keys():
            print(f"{group} has {len(groupDict[group])} items")
        print("\nchecking if there is any crossover between groups...")
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

def makeURNListFromGroupDict(groupDict):
    ''' returns dict with list of URNs
    i.e. {'xbb':[182274, 123423,...],...}    '''
    dictOfURNs = {}
    for group in groupDict.keys():
        dictOfURNs[group] = []
        for school in groupDict[group]:
            dictOfURNs[group].append(school.getURN())
    return dictOfURNs



def makeLabelledSubsets(dictOfURNGroups, cat1, cat2, df, write=''):
    """Add a column called Stuck to the df
    1 if the URN is in the 'stuck' list
    0 if not stuck
    If write != False then write to .csv
    """
    import creatingAMonster as cam
    print("Adding/updating stuck column in df...")
    posURNs, negURNs = dictOfURNGroups[cat1], dictOfURNGroups[cat2]
    allURNs = posURNs + negURNs
    URNsToDrop = set(df['URN']) - set(allURNs)
    df = df[~df['URN'].isin(URNsToDrop)]
    df["Class"] = df.apply(
        lambda row: np.where((int(row["URN"]) in posURNs), 1, 0), axis=1
    )
    df = cam.dropColsFromList(df, ['Stuck'])
    if len(write) >0:
        df.to_csv(write)
    return  df

dictOfURNs = makeURNListFromGroupDict(
    newGrouping(openSchoolDict, True)
)
inputDF = pd.read_csv('dfForModelModifiedImputedWithPTRWM.csv')
#dfWithCats = makeLabelledSubsets(dictOfURNs, 'bbb','gbb',inputDF, 'bbbVgbbLessCols.csv')
#dfWithCats = makeLabelledSubsets(dictOfURNs, 'bbbb','gbbb',inputDF, 'bbbbVgbbbLessCols.csv')
#dfWithCats = makeLabelledSubsets(dictOfURNs, 'bbb','gsbbs', inputDF, 'bbbVgsbbsLessCols.csv')
dfWithCats = makeLabelledSubsets(dictOfURNs, 'bbbb','gsbbbs', inputDF, 'bbbbVgsbbbsWithPTRWM.csv')
