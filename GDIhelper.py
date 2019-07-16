# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:28:59 2019

@author: reesc1
"""
import setFolder as sf
import colNames as cn
import pandas as pd
### PERFORMANCE DATA ########################################################
perfNames = []
perfDict = {}
for y in ["y18", "y16", "y14"]:
    for ks in ["ks2", "ks4", "ks5"]:
        perfNames.append(y + ks)
        perfDict[y + ks] = {
            "df": pd.DataFrame(),
            "path": None,
            "toKeep": [],
            "toFloat": [],
            "toPct": [],
            "mergeName": None,
            "ignore": False,
            "stackOn": None,
        }
# ['y18ks2', 'y18ks4', 'y16ks2', 'y16ks4', 'y14ks2', 'y14ks4']
perfPaths = [
    r"\2017-2018\Performance\england_ks2final.csv",
    r"\2017-2018\Performance\england_ks4final.csv",
    r"\2017-2018\Performance\england_ks5final.csv",
    r"\2015-2016\Performance\england_ks2final.csv",
    r"\2015-2016\Performance\england_ks4final.csv",
    r"\2015-2016\Performance\england_ks5final.csv",
    r"\2013-2014\Performance\england_ks2final.csv",
    r"\2013-2014\Performance\england_ks4final.csv",
    r"\2013-2014\Performance\england_ks5final.csv",
]
for i, name in enumerate(perfNames):
    perfDict[name]["path"] = perfPaths[i]
    perfDict[name]["toKeep"] = cn.PerfColsToKeep
    perfDict[name]["toFloat"] = ["URN", "TOTPUPS"]
    perfDict[name]["toPct"] = ["RELDENOM", "AGERANGE"]
    perfDict[name]["mergeName"] = "_" + name[1:3]
    if name[-1] == "5":
        perfDict[name]["ignore"] = True
    if name[-1] == "4":
        perfDict[name]["stackOn"] = name[:-1] + "2"



### CENSUS DATA ##############################################################

censusNames = []
censusDict = {}
for y in ["y18", "y16", "y14"]:
    censusNames.append(y)
    censusDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
    }

censusPaths = [
        r"\2017-2018\Absence and Pupil Population\england_census.csv",
        r"\2015-2016\Absence and Pupil Population\england_census.csv",
        r"\2013-2014\Absence and Pupil Population\england_census.csv"
        ]
for i, name in enumerate(censusNames):
    cd = censusDict[name]
    cd["path"] = censusPaths[i]
    cd["toKeep"] = cn.CensusColsToKeep
    cd["toFloat"] = ["URN",'LA','ESTAB','NOR']
    cd["toPct"] = []
    cd["mergeName"] = "_" + name[1:3]
