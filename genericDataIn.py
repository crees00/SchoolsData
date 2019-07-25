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
print(f"running genericDataIn from {sf.where} at {start}")
# Load dictionaries giving all the needed info
perfDict = GDIh.perfDict
censusDict = GDIh.censusDict
absDict = GDIh.absDict
spineDict = GDIh.spineDict
swfDict = GDIh.swfDict
cfrDict = GDIh.cfrDict
sfbDict = GDIh.sfbDict


def readData(dataDict):
    startReading = datetime.datetime.now()
    for name in dataDict.keys():
        dataDict[name]["df"] = pd.read_csv(
            sf.homeFolder + dataDict[name]["path"], encoding="latin-1"
        )
        print('\n\n',name,'\n')
        for col in dataDict[name]['df'].columns:
            if col in ['p8mea','att8scr','perfirchoice16']:
                print(name, col)

    print(f"data loaded - took {datetime.datetime.now()-startReading}")
    return dataDict


print("updating dfs..")


def colChop(df, toKeep, name):
    nowKeep = []
    blanks = []
    for listOfCols in toKeep:
        if type(listOfCols) == str:
            if listOfCols in df.columns:
                nowKeep.append(listOfCols)
            else:
                blanks.append(listOfCols)
        else:
            addedOne = False
            for col in listOfCols:
                if col in df.columns:
                    nowKeep.append(col)
                    addedOne = True
            if addedOne == False:
                blanks.append(listOfCols[0])
    if len(nowKeep) == len(toKeep):
        return df[nowKeep]
    else:
        print(f"\nError - only {len(nowKeep)} of {len(toKeep)} cols found")
        print(f"nowKeep: {nowKeep}\ntoKeep: {toKeep}")
        print(f"blanks: {blanks}")
        # ks2 has some cols that don't match with ks4 so return it anyway with 
        # nans in cols which it doesn't share. Keep the cols to keep the dims
        # of the df to stop problems later
        if name[-3:] == 'ks2':
            print(f"returning df anyway with cols {nowKeep+blanks}")
            for blank in blanks:
                df[blank] = np.nan
            return df[nowKeep + blanks]


def feedToColChop(dataDict):
    """ Just sends dfs to colChop to remove cols"""
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == False:
            dataDict[name]["df"] = colChop(
                dataDict[name]["df"], dataDict[name]["toKeep"], name
            )
    return dataDict


def tidyUp(dataDict):
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == True:
            continue
        df = dataDict[name]["df"]
        for column in df.columns:
            if column not in (
                set(dataDict[name]["toFloat"])
                | set(dataDict[name]["toPct"])
                | set(dataDict[name]["toCurr"])
            ):
                try:
                    df[column].replace({" ": np.nan}, inplace=True)
                except TypeError:
                    print(f'{column} in {name} not replacing " "')
    return dataDict


def fixCols(dataDict):
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == False:
            df = dataDict[name]["df"]
            for col in df.columns:
                if col in dataDict[name]["toFloat"]:
                    try:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                    except ValueError:
                        print(f"{col} in {name} not converting")
                elif col in dataDict[name]["toPct"]:
                    df[col].astype(str)
                    df[col] = df[col].apply(cam.p2f)
                elif col in dataDict[name]["toCurr"]:
                    df[col].astype(str)
                    df[col] = df[col].apply(cam.c2f)
                else:
                    df[col].astype(str)
    return dataDict


def allInOne(dataDict):
    return tidyUp(fixCols(feedToColChop(readData(dataDict))))


def mergeVertical(ks2df, ks4df, year):
    """ take ks2 and ks4 rows for the same year and stack them. 
    For schools which have both ks2 and ks4, take the line from ks4 """
#    print(f"ks2dfcols:\n{ks2df.columns}")
#    print(f"ks4dfcols:\n{ks4df.columns}")
    newColDict = dict(zip(ks4df.columns, ks2df.columns))
#    print(f"newColDict:\n{newColDict}")
    stackedDF = pd.concat([ks2df, ks4df.rename(columns=newColDict)], ignore_index=True)
    finColNames = [x + "_" + str(year) for x in stackedDF.columns if x != "URN"]
    finColNames.insert(0, "URN")
#    print(finColNames)
    finColDict = dict(zip(stackedDF.columns, finColNames))
    stackedDF = stackedDF.rename(columns=finColDict)
    stackedDF["URN"].astype(float)
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
    if len(outDFs) == 0:
        for name in dataDict.keys():
            if dataDict[name]["ignore"] == False:
                outDFs.append(name)
    return outDFs


def addToMainDF(dfToAddTo, dataDict, write=False):
    listOfDFs = feedToMergeVertical(dataDict)
    dfNew = dfToAddTo
    for dfOrName in listOfDFs:
        URNs = set(dfNew["URN"])
        if type(dfOrName) == str:
            df = dataDict[dfOrName]["df"]
            dfSubset = df.drop_duplicates(subset=["URN"])
            dfNew = dfNew.merge(
                dfSubset,
                on="URN",
                how="left",
                sort=True,
                suffixes=("", dataDict[dfOrName]["mergeName"]),
            )
            print(f"{len(set(dfSubset['URN']))} to {len(set(dfNew['URN']))}")
            print(
                f"after adding {dfOrName} with shape {dataDict[dfOrName]['df'].shape} has shape {dfNew.shape}"
            )

        else:
            df = dfOrName
            dfSubset = df.drop_duplicates(subset=["URN"])
            dfNew = dfNew.merge(dfSubset, on="URN", how="left", sort=True)
            print(f"{len(set(dfOrName['URN']))} to {len(set(dfNew['URN']))}")
            print(f"after adding {dfOrName.shape} has shape {dfNew.shape}")

    #    df5 = df5.sort_values(by='URN', axis=1)
    if write:
        dfNew.to_csv("df5.csv")

    return dfNew


def runAll(dataDict, dfToAddTo, write=False):
    startOfRunAll = datetime.datetime.now()
    dataDict = allInOne(dataDict)
    df = addToMainDF(dfToAddTo, dataDict, write)
    print(f"runAll took {datetime.datetime.now()-startOfRunAll}")
    return df


df4 = pd.read_csv("df4.csv")
df5 = runAll(perfDict, df4, False)
#df6 = runAll(censusDict, df5, True)
#df7 = runAll(absDict, df6, True)
#df8 = runAll(spineDict, df7, True)
#df9 = runAll(swfDict, df8, True)
#df10 = runAll(cfrDict, df9, True)
df11 = runAll(sfbDict, df5, False)
print(f"genericDataIn complete - took {datetime.datetime.now()-start}")
