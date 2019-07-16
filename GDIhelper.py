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
    perfDict[name]["toPct"] = set([item for sublist in cn.PerfColsToKeep for item in sublist])-{"RELDENOM", "AGERANGE",'URN','TOTPUPS'}
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
    cd["toFloat"] = ["URN",'LA','ESTAB','NOR','TOTPUPSENDN','PNUMEAL','PNUMFSM']
    cd["toPct"] = []
    cd["mergeName"] = "_" + name[1:3]


### ABSENCE DATA #############################################################
absNames = []
absDict = {}
for y in ["y18", "y16", "y14"]:
    absNames.append(y)
    absDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
    }

absPaths = [
        r"\2017-2018\Absence and Pupil Population\england_abs.csv",
        r"\2015-2016\Absence and Pupil Population\england_abs.csv",
        r"\2013-2014\Absence and Pupil Population\england_abs.csv"
        ]
for i, name in enumerate(absNames):
    ad = absDict[name]
    ad["path"] = absPaths[i]
    ad["toKeep"] = cn.AbsenceColsToKeep
    ad["toFloat"] = ["URN",'PERCTOT']
    ad["toPct"] = []#,'PERCTOT','PPERSABS10']
    ad["mergeName"] = "_" + name[1:3]


### SPINE DATA ###############################################################
spineNames = []
spineDict = {}
for y in ["y18", "y16", "y14"]:
    spineNames.append(y)
    spineDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
    }

spinePaths = [
        r"\2017-2018\General School Information\england_spine.csv",
        r"\2015-2016\General School Information\england_spine.csv",
        r"\2013-2014\General School Information\england_spine.csv"
        ]
for i, name in enumerate(spineNames):
    ad = spineDict[name]
    ad["path"] = spinePaths[i]
    ad["toKeep"] = cn.SpineColsToKeep
    ad["toFloat"] = ["URN",'AGEL','AGEH','ISPRIMARY','ISSECONDARY','ISPOST16']
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]

### SWF DATA #################################################################
swfNames = []
swfDict = {}
for y in ["y18", "y16", "y14"]:
    swfNames.append(y)
    swfDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
    }

swfPaths = [
        r"\2017-2018\Workforce and Finance\england_swf.csv",
        r"\2015-2016\Workforce and Finance\england_swf.csv",
        r"\2013-2014\Workforce and Finance\england_swf.csv"
        ]
for i, name in enumerate(swfNames):
    ad = swfDict[name]
    ad["path"] = swfPaths[i]
    ad["toKeep"] = cn.swfColsToKeep
    ad["toFloat"] = ["URN",'Pupil:     Teacher Ratio','Mean Gross FTE Salary of All Teachers (£s)']
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]
