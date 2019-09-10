# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:52:17 2019

data in: df4.csv from creatingAMonster.py
data out: df5.csv used by pickColsToUse.py

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
fin18Dict = GDIh.fin18Dict
fin17Dict = GDIh.fin17Dict

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
        print(dataDict[name]['df'].columns)
        print(dataDict[name]["toKeep"])
    print(f"data for {name} loaded - took {datetime.datetime.now()-startReading}")
    return dataDict


print("updating dfs..")


def colChop(df, toKeep, name):
    nowKeep = []
    blanks = []
    print(f"toKeep for {name}:\n{toKeep}")
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
        print("running feedToColChop for",name, "with shape",dataDict[name]["df"].shape)
        print("toKeep from dataDict:\n",dataDict[name]["toKeep"])
        if dataDict[name]["ignore"] == False:
            dataDict[name]["df"] = colChop(
                dataDict[name]["df"], dataDict[name]["toKeep"], name
            )
        print("after feedToColChop",name, "has shape",dataDict[name]["df"].shape)
    return dataDict


def tidyUp(dataDict):
    for name in dataDict.keys():
        print("running tidyUp for",name)
        if dataDict[name]["ignore"] == True:
            continue
        df = dataDict[name]["df"]
        print(df.shape)
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
        mergeCol = "URN"
        URNs = set(dfNew["URN"])
        if type(dfOrName) == str:
            df = dataDict[dfOrName]["df"]
            print(df.columns)
            if "URN" not in df.columns:
                mergeCol = "LAESTAB"
            dfSubset = df.drop_duplicates(subset=[mergeCol])
            print('size of dfSubset',dfSubset.shape)
            print('dfSubset cols:', dfSubset.columns)
            dfNew = dfNew.merge(
                dfSubset,
                on=mergeCol,
                how="left",
                sort=True,
                suffixes=("", dataDict[dfOrName]["mergeName"]),
            )
            print(f"{len(set(dfSubset[mergeCol]))} to {len(set(dfNew[mergeCol]))}")
            print(
                f"after adding {dfOrName} with shape {dataDict[dfOrName]['df'].shape} has shape {dfNew.shape}"
            )

        else:
            df = dfOrName
            dfSubset = df.drop_duplicates(subset=[mergeCol])
            dfNew = dfNew.merge(dfSubset, on=mergeCol, how="left", sort=True)
            print(f"{len(set(dfOrName[mergeCol]))} to {len(set(dfNew[mergeCol]))}")
            print(f"after adding {dfOrName.shape} has shape {dfNew.shape}")

    #    df5 = df5.sort_values(by='URN', axis=1)
    if write:
        dfNew.to_csv("df5.csv")

    return dfNew

def fixPerfCol(df, write=''):
    ''' Attainment measures not dealt with correctly in previous code - 
    ks4: ATT8SCR - score based on exam results
    ks2: PTRWM or variant - percentage of pupils with a certain level in reading/writing/maths
    ATT8SCR was treated as a percentage but it is a score itself
    
    This func takes ATT8SCR and ranks all schools which have a score, then 
    converts rank into % so e.g. mid performing school will have score of 50%,
    school with worst ATT8SCR will have 0%.
    
    Apply same logic to read/write/maths scores, so end up with all ks2 and ks4 
    schools having a ranking score from 0 to 1. 
    Then just combine into one col and add to df    
    '''

    ks4perf18 = pd.read_csv(
            sf.homeFolder +  r"\2017-2018\Performance\england_ks4final.csv", encoding="latin-1")
    ks2perf18 = pd.read_csv(
            sf.homeFolder + r"\2017-2018\Performance\england_ks2final.csv", encoding = "latin-1")
    rwmSubset = ks2perf18[['URN','PTRWM_EXP']]
    att8Subset = ks4perf18[['URN','ATT8SCR']]
    
    # Remove rows with blanks
    rwmSubset['URN'] = pd.to_numeric(rwmSubset['URN'], errors='coerce')
    att8Subset['ATT8SCR'] = pd.to_numeric(att8Subset['ATT8SCR'],errors='coerce')
    att8Subset.dropna(inplace=True)

    # Make ranking col for ks2 data
    rwmSubset['PTRWM_EXP']=rwmSubset['PTRWM_EXP'].astype(str)
    rwmSubset['PTRWM_EXP'] = rwmSubset['PTRWM_EXP'].apply(cam.p2f) 
    rwmSubset.dropna(inplace=True)
    rwmSubset['PTRWMpctRank'] = (rwmSubset['PTRWM_EXP'].rank(ascending=True))/len(rwmSubset)
    
    # Make ranking col for ks4 data
    att8Subset['ATT8SCRpctRank'] = (att8Subset['ATT8SCR'].rank(ascending=True)) / len(att8Subset)
    
    # Merge new cols onto input large df
    df = df.merge(how='left',right=att8Subset.drop('ATT8SCR', axis=1), on='URN')
    df = df.merge(how='left',right=rwmSubset.drop('PTRWM_EXP', axis=1), on='URN')
    
    # Merge two new cols to give one col - if vals in both cols, take a mean
    df['PerformancePctRank'] = np.nanmean([df['PTRWMpctRank'],df['ATT8SCRpctRank']],axis=0)
    df.drop(['ATT8SCRpctRank','PTRWMpctRank'], axis=1, inplace=True)
    
    if len(write)>0:
        df.to_csv(write)
    return df
    
def runAll(dataDict, dfToAddTo, write=False):
    startOfRunAll = datetime.datetime.now()
    dataDict = allInOne(dataDict)
    df = addToMainDF(dfToAddTo, dataDict, write)
    print(f"runAll took {datetime.datetime.now()-startOfRunAll}")
    return df



#df4 = pd.read_csv("df4.csv")
#df5 = runAll(perfDict, df4)
#df6 = runAll(censusDict, df5)
#df7 = runAll(absDict, df6)
#df8 = runAll(spineDict, df7)
#df9 = runAll(swfDict, df8)
##df10 = runAll(cfrDict, df9, True)
##df11 = runAll(sfbDict, df9, True)
df12 = runAll(fin18Dict, pd.read_csv("df5 - copy.csv"))
df13 = runAll(fin17Dict, df12, True)
df14 = fixPerfCol(df13, 'df5AllColsPreImputed.csv')

print(f"genericDataIn complete - took {datetime.datetime.now()-start}")
