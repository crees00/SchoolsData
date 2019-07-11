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


perfDF18ks2 = pd.read_csv(
    sf.perfFolder + r"\2017-2018\Performance\england_ks2final.csv", encoding="latin-1"
)
perfDF18ks4 = pd.read_csv(
    sf.perfFolder + r"\2017-2018\Performance\england_ks4final.csv", encoding="latin-1"
)
perfDF18ks5 = pd.read_csv(
    sf.perfFolder + r"\2017-2018\Performance\england_ks5final.csv", encoding="latin-1"
)

perfDF16ks2 = pd.read_csv(
    sf.perfFolder + r"\2015-2016\Performance\england_ks2final.csv", encoding="latin-1"
)
perfDF16ks4 = pd.read_csv(
    sf.perfFolder + r"\2015-2016\Performance\england_ks4final.csv", encoding="latin-1"
)
perfDF16ks5 = pd.read_csv(
    sf.perfFolder + r"\2015-2016\Performance\england_ks5final.csv", encoding="latin-1"
)

perfDF14ks2 = pd.read_csv(
    sf.perfFolder + r"\2013-2014\Performance\england_ks2final.csv", encoding="latin-1"
)
perfDF14ks4 = pd.read_csv(
    sf.perfFolder + r"\2013-2014\Performance\england_ks4final.csv", encoding="latin-1"
)
perfDF14ks5 = pd.read_csv(
    sf.perfFolder + r"\2013-2014\Performance\england_ks5final.csv", encoding="latin-1"
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


# for item in dfDict.keys():
#    print(item)
#    dfDict[item] = colChop(dfDict[item])
#    dfDict[item] = tidyUp(dfDict[item])
#    dfDict[item] = fixCols(dfDict[item])

perfDF18ks2 = allInOne(perfDF18ks2)
perfDF16ks2 = allInOne(perfDF16ks2)
perfDF14ks2 = allInOne(perfDF14ks2)
perfDF18ks4 = allInOne(perfDF18ks4)
perfDF16ks4 = allInOne(perfDF16ks4)
perfDF14ks4 = allInOne(perfDF14ks4)

# perfDF18ks2 = tidyUp(perfDF18ks2)
# perfDF16ks2 = tidyUp(perfDF16ks2)
# perfDF14ks2 = tidyUp(perfDF14ks2)
#
# perfDF18ks2 = fixCols(perfDF18ks2)
# perfDF16ks2 = fixCols(perfDF16ks2)
# perfDF14ks2 = fixCols(perfDF14ks2)

# perfDF18ks2 = fixCols(tidyUp(allInOne(perfDF18ks2)))

## Add performance data
# perfDF18ks2['URN'].astype(float)
# df5 = df4.merge(
#        perfDF18ks2,
#        on='URN',
#        how="left",
# )
