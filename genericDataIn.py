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
# Load dictionaries giving all the needed info
perfDict = GDIh.perfDict
censusDict = GDIh.censusDict
absDict = GDIh.absDict
spineDict = GDIh.spineDict

def readData(dataDict):
    startReading = datetime.datetime.now()
    for name in dataDict.keys():
        dataDict[name]["df"] = pd.read_csv(
            sf.homeFolder + dataDict[name]["path"], encoding="latin-1"
        )
    print(f"data loaded - took {datetime.datetime.now()-startReading}")
    return dataDict

print("updating dfs..")

def colChop(df, toKeep):
    nowKeep = []
    for listOfCols in toKeep:
        if type(listOfCols)==str:
            if listOfCols in df.columns:
                nowKeep.append(listOfCols)
        for col in listOfCols:
            if col in df.columns:
                nowKeep.append(col)
    if len(nowKeep) == len(toKeep):
        return df[nowKeep]
    else:
        print(f"\nError - only {len(nowKeep)} of {len(toKeep)} cols found")
        print(f"nowKeep: {nowKeep}\ntoKeep: {toKeep}")
        print(f'{set(toKeep)-set(nowKeep)} missing')


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
        if dataDict[name]['ignore'] == True:
            continue
        df = dataDict[name]["df"]
        for column in df.columns:
            if column not in (set(dataDict[name]['toFloat']) | set(dataDict[name]['toPct'])):
                try:
                    df[column].replace({" ": np.nan}, inplace=True)
                except TypeError:
                    print(f'{column} in {name} not replacing " "')
#            if "TOTPUPS" in df.columns:
#                df["TOTPUPS"].replace({"NEW": np.nan}, inplace=True)
#                df["TOTPUPS"].replace({"NP": np.nan}, inplace=True)
        # get rid of text in cols that are being turned to floats
#        for col in dataDict[name]['toFloat']:
#            df[col].replace({"[a-zA-Z]+": np.nan}, inplace=True, regex=True)
#            except:
#                pass
    return dataDict


def fixCols(dataDict):
    for name in dataDict.keys():
        if dataDict[name]["ignore"] == False:
            df = dataDict[name]["df"]
            for col in df.columns:
                if col in dataDict[name]["toFloat"]:
#                    print(col)
#                    df[col] = df[col].astype(float)
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except ValueError:
                        print(f'{col} in {name} not converting')
                elif col in dataDict[name]["toPct"]:
                    df[col].astype(str)
                    df[col] = df[col].apply(cam.p2f)
    return dataDict


def allInOne(dataDict):
    return tidyUp(fixCols(feedToColChop(readData(dataDict))))


#perfDict = allInOne(perfDict)


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
    if len(outDFs)==0:
        for name in dataDict.keys():
            if dataDict[name]['ignore']==False:
                outDFs.append(name)
    return outDFs


def addToMainDF(dfToAddTo, dataDict, write=False):
    listOfDFs = feedToMergeVertical(dataDict)
    dfNew = dfToAddTo
    for dfOrName in listOfDFs:
        if type(dfOrName)==str:
            dfNew = dfNew.merge(dataDict[dfOrName]['df'], on="URN", how="left", 
                            sort=True, suffixes = ("",dataDict[dfOrName]['mergeName']))
        else:
            dfNew = dfNew.merge(dfOrName, on='URN', how='left', sort=True)
    #    df5 = df5.sort_values(by='URN', axis=1)
        print(f'after adding {dfOrName} has shape {dfNew.shape}')
    if write:
        dfNew.to_csv("df5.csv")
        
    return dfNew


def runAll(dataDict, dfToAddTo, write=False):
    dataDict = allInOne(dataDict)
    return addToMainDF(dfToAddTo,dataDict, write)


df4 = pd.read_csv("df4.csv")
df5 = runAll(perfDict,df4, True )
df6 = runAll(censusDict,df5,True)
df7 = runAll(absDict,df6,True)
df8 = runAll(spineDict, df7, True)
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

print(f"genericDataIn complete - took {datetime.datetime.now()-start}")
