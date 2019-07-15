# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:52:17 2019

@author: reesc1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:48:13 2019

@author: Chris
"""

import pandas as pd
import numpy as np
import setFolder as sf
import colNames as cn
import creatingAMonster as cam
import datetime
import findStuck
import copy
import GDIhelper as GDIh

start = datetime.datetime.now()
print(f"running genericDataIn at {start}")
perfDict = GDIh.perfDict
censusDict = GDIh.censusDict

def readData(dataDict):
    for name in dataDict.keys():
        dataDict[name]["df"] = pd.read_csv(
            sf.homeFolder + dataDict[name]["path"], encoding="latin-1"
        )
    print(f"data loaded - took {datetime.datetime.now()-start}")
    return dataDict

print("updating dfs..")

def colChop(df, toKeep):
    nowKeep = []
    for listOfCols in toKeep:
        for col in listOfCols:
            if col in df.columns:
                nowKeep.append(col)
    if len(nowKeep) == len(toKeep):
        return df[nowKeep]
    else:
        print(f"\nError - only {len(nowKeep)} of {len(toKeep)} cols found")
        print(f"nowKeep: {nowKeep}\ntoKeep: {toKeep}")


def feedToColChop(dataDict):
    """ Just sends dfs to colChop to remove cols"""
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == False:
            dataDict[name]["df"] = colChop(
                dataDict[name]["df"], dataDict[name]["toKeep"]
            )
    return dataDict


def tidyUp(dataDict):
    for name in dataDict.keys():
        df = dataDict[name]["df"]
        df.replace({" ": np.nan}, inplace=True)
        if "TOTPUPS" in df.columns:
            df["TOTPUPS"].replace({"NEW": np.nan}, inplace=True)
            df["TOTPUPS"].replace({"NP": np.nan}, inplace=True)
    return dataDict


def fixCols(dataDict):
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == False:
            df = dataDict[name]["df"]
            for col in df.columns:
                if col in dataDict[name]["toFloat"]:
                    df[col] = df[col].astype(float)

                #            try:
                #                df[col] = df[col].astype(float)
                #            except ValueError:
                #                print(f'{col} in df not converting')
                elif col not in dataDict[name]["toPct"]:
                    df[col].astype(str)
                    df[col] = df[col].apply(cam.p2f)
    return dataDict


def allInOne(dataDict):
    return fixCols(tidyUp(feedToColChop(readData(dataDict))))


perfDict = allInOne(perfDict)


def mergeVertical(ks2df, ks4df, year):
    """ take ks2 and ks4 rows for the same year and stack them. 
    For schools which have both ks2 and ks4, take the line from ks4 """
    print(f"ks2dfcols:\n{ks2df.columns}")
    print(f"ks4dfcols:\n{ks4df.columns}")
    newColDict = dict(zip(ks4df.columns, ks2df.columns))
    print(f"newColDict:\n{newColDict}")
    stackedDF = pd.concat([ks2df, ks4df.rename(columns=newColDict)], ignore_index=True)
    finColNames = [x + "_" + str(year) for x in stackedDF.columns if x != "URN"]
    finColNames.insert(0, "URN")
    print(finColNames)
    finColDict = dict(zip(stackedDF.columns, finColNames))
    stackedDF = stackedDF.rename(columns=finColDict)
    stackedDF["URN"].astype(float)
    cam.analyseCols(stackedDF)
    return stackedDF


def feedToMergeVertical(dataDict):
    outDFs = []
    for name in dataDict.keys():
        if dataDict[name]["stackOn"] != None:
            outDFs.append(
                mergeVertical(
                    dataDict[dataDict[name]["stackOn"]]["df"],
                    dataDict[name]["df"],
                    dataDict[name]["mergeName"],
                )
            )
    return outDFs


def addToMainDF(listOfDFs, dfToAddTo, write=False):
    df5 = dfToAddTo  # .copy.deepcopy()
    for df in listOfDFs:
        df5 = df5.merge(df, on="URN", how="left", sort=True)
    #    df5 = df5.sort_values(by='URN', axis=1)
    if write:
        df5.to_csv("df5.csv")
    return df5


def runAll(dataDict, dfToAddTo, write=False):
    dataDict = allInOne(dataDict)
    return addToMainDF(feedToMergeVertical(dataDict), dfToAddTo, write)


df4 = pd.read_csv("df4.csv")
df5 = runAll(censusDict, df4, True)
#    perfDF18ks2, perfDF18ks4, perfDF18ks5, perfDF16ks2, perfDF16ks4, perfDF16ks5, perfDF14ks2, perfDF14ks4, perfDF14ks5 = (
#        readPerfData()
#    )
#    perfDF18ks2 = allInOne(perfDF18ks2)
#    perfDF16ks2 = allInOne(perfDF16ks2)
#    perfDF14ks2 = allInOne(perfDF14ks2)
#    perfDF18ks4 = allInOne(perfDF18ks4)
#    perfDF16ks4 = allInOne(perfDF16ks4)
#    perfDF14ks4 = allInOne(perfDF14ks4)
#
#    perfDF18 = findStuck.generateDFs(mergeVertical(perfDF18ks2, perfDF18ks4, 18))
#    perfDF16 = findStuck.generateDFs(mergeVertical(perfDF16ks2, perfDF16ks4, 16))
#    perfDF14 = findStuck.generateDFs(mergeVertical(perfDF14ks2, perfDF14ks4, 14))

#    return addPerfData([perfDF18, perfDF16, perfDF14], write)


# df5 = addPerfData([perfDF18, perfDF16, perfDF14], True)
# runAllPerf(True)
# Add performance data
# perfDF18ks2['URN'].astype(float)

print(f"perfData complete - took {datetime.datetime.now()-start}")
