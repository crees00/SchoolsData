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

start = datetime.datetime.now()
print(f"running perfData at {start}")


def readPerfData():
    perfDF18ks2 = pd.read_csv(
        sf.homeFolder + r"\2017-2018\Performance\england_ks2final.csv",
        encoding="latin-1",
    )
    perfDF18ks4 = pd.read_csv(
        sf.homeFolder + r"\2017-2018\Performance\england_ks4final.csv",
        encoding="latin-1",
    )
    perfDF18ks5 = pd.read_csv(
        sf.homeFolder + r"\2017-2018\Performance\england_ks5final.csv",
        encoding="latin-1",
    )

    perfDF16ks2 = pd.read_csv(
        sf.homeFolder + r"\2015-2016\Performance\england_ks2final.csv",
        encoding="latin-1",
    )
    perfDF16ks4 = pd.read_csv(
        sf.homeFolder + r"\2015-2016\Performance\england_ks4final.csv",
        encoding="latin-1",
    )
    perfDF16ks5 = pd.read_csv(
        sf.homeFolder + r"\2015-2016\Performance\england_ks5final.csv",
        encoding="latin-1",
    )

    perfDF14ks2 = pd.read_csv(
        sf.homeFolder + r"\2013-2014\Performance\england_ks2final.csv",
        encoding="latin-1",
    )
    perfDF14ks4 = pd.read_csv(
        sf.homeFolder + r"\2013-2014\Performance\england_ks4final.csv",
        encoding="latin-1",
    )
    perfDF14ks5 = pd.read_csv(
        sf.homeFolder + r"\2013-2014\Performance\england_ks5final.csv",
        encoding="latin-1",
    )
    print(f"data loaded - took {datetime.datetime.now()-start}")
    return (
        perfDF18ks2,
        perfDF18ks4,
        perfDF18ks5,
        perfDF16ks2,
        perfDF16ks4,
        perfDF16ks5,
        perfDF14ks2,
        perfDF14ks4,
        perfDF14ks5,
    )


print("updating dfs..")


def colChop(df):
    nowKeep = []
    toKeep = cn.PerfColsToKeep
    for listOfCols in toKeep:
        for col in listOfCols:
            if col in df.columns:
                nowKeep.append(col)
    if len(nowKeep) == len(toKeep):
        return df[nowKeep]
    else:
        print(f"\nError - only {len(nowKeep)} of {len(toKeep)} cols found")
        print(f"nowKeep: {nowKeep}\ntoKeep: {toKeep}")


def tidyUp(df):
    df.replace({" ": np.nan}, inplace=True)
    df["TOTPUPS"].replace({"NEW": np.nan}, inplace=True)
    df["TOTPUPS"].replace({"NP": np.nan}, inplace=True)
    return df


def fixCols(df):
    for col in df.columns:
        if col in ["URN", "TOTPUPS"]:
            df[col] = df[col].astype(float)

        #            try:
        #                df[col] = df[col].astype(float)
        #            except ValueError:
        #                print(f'{col} in df not converting')
        elif col not in ["RELDENOM", "AGERANGE"]:
            df[col].astype(str)
            df[col] = df[col].apply(cam.p2f)
    return df


def allInOne(df):
    return fixCols(tidyUp(colChop(df)))


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


def addPerfData(listOfDFs, write=False):
    df5 = cam.df4  # .copy.deepcopy()
    for df in listOfDFs:
        df5 = df5.merge(df, on="URN", how="left", sort=True)
#    df5 = df5.sort_values(by='URN', axis=1)
    if write:
        df5.to_csv("df5.csv")
    return df5


def runAllPerf(write=False):
    perfDF18ks2, perfDF18ks4, perfDF18ks5, perfDF16ks2, perfDF16ks4, perfDF16ks5, perfDF14ks2, perfDF14ks4, perfDF14ks5 = (
        readPerfData()
    )
    perfDF18ks2 = allInOne(perfDF18ks2)
    perfDF16ks2 = allInOne(perfDF16ks2)
    perfDF14ks2 = allInOne(perfDF14ks2)
    perfDF18ks4 = allInOne(perfDF18ks4)
    perfDF16ks4 = allInOne(perfDF16ks4)
    perfDF14ks4 = allInOne(perfDF14ks4)

    perfDF18 = findStuck.generateDFs(mergeVertical(perfDF18ks2, perfDF18ks4, 18))
    perfDF16 = findStuck.generateDFs(mergeVertical(perfDF16ks2, perfDF16ks4, 16))
    perfDF14 = findStuck.generateDFs(mergeVertical(perfDF14ks2, perfDF14ks4, 14))

    return addPerfData([perfDF18, perfDF16, perfDF14], write)

#df5 = addPerfData([perfDF18, perfDF16, perfDF14], True)
runAllPerf(True)
# Add performance data
# perfDF18ks2['URN'].astype(float)

print(f"perfData complete - took {datetime.datetime.now()-start}")
