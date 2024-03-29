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
            "toCurr": [],
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
    perfDict[name]["toKeep"] = cn.PerfColsToKeep.copy()
#    print(name, perfDict[name]["toKeep"])
    if name[-3:] == 'ks4':
        for subList in cn.Perfks4ColsToKeep:
#            print('\n',name)
#            print('sublist:',subList)
#            print('\ntoKeep before:',perfDict[name]["toKeep"])
            perfDict[name]["toKeep"].append(subList)
#            print('\ntoKeep after:',perfDict[name]["toKeep"])
    perfDict[name]["toFloat"] = ["URN", "TOTPUPS"]
    perfDict[name]["toPct"] = set(
        [item for sublist in cn.PerfColsToKeep for item in sublist]
    ) - {"RELDENOM", "AGERANGE", "URN", "TOTPUPS"}
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
        "toCurr": [],
    }

censusPaths = [
    r"\2017-2018\Absence and Pupil Population\england_census.csv",
    r"\2015-2016\Absence and Pupil Population\england_census.csv",
    r"\2013-2014\Absence and Pupil Population\england_census.csv",
]
for i, name in enumerate(censusNames):
    cd = censusDict[name]
    cd["path"] = censusPaths[i]
    cd["toKeep"] = cn.CensusColsToKeep
    cd["toFloat"] = ["URN", "LA", "ESTAB", "NOR", "TOTPUPSENDN", "PNUMEAL", "PNUMFSM"]
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
        "toCurr": [],
    }

absPaths = [
    r"\2017-2018\Absence and Pupil Population\england_abs.csv",
    r"\2015-2016\Absence and Pupil Population\england_abs.csv",
    r"\2013-2014\Absence and Pupil Population\england_abs.csv",
]
for i, name in enumerate(absNames):
    ad = absDict[name]
    ad["path"] = absPaths[i]
    ad["toKeep"] = cn.AbsenceColsToKeep
    ad["toFloat"] = ["URN", "PERCTOT"]
    ad["toPct"] = []  # ,'PERCTOT','PPERSABS10']
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
        "toCurr": [],
    }

spinePaths = [
    r"\2017-2018\General School Information\england_spine.csv",
    r"\2015-2016\General School Information\england_spine.csv",
    r"\2013-2014\General School Information\england_spine.csv",
]
for i, name in enumerate(spineNames):
    ad = spineDict[name]
    ad["path"] = spinePaths[i]
    ad["toKeep"] = cn.SpineColsToKeep
    ad["toFloat"] = ["URN", "AGEL", "AGEH", "ISPRIMARY", "ISSECONDARY", "ISPOST16"]
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
        "toCurr": [],
    }

swfPaths = [
    r"\2017-2018\Workforce and Finance\england_swf.csv",
    r"\2015-2016\Workforce and Finance\england_swf.csv",
    r"\2013-2014\Workforce and Finance\england_swf.csv",
]
for i, name in enumerate(swfNames):
    ad = swfDict[name]
    ad["path"] = swfPaths[i]
    ad["toKeep"] = cn.swfColsToKeep
    ad["toFloat"] = ["URN", "Pupil:     Teacher Ratio", "RATPUPTEA"]
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]
    ad["toCurr"] = [
        "Mean Gross FTE Salary of All Teachers (£s)",
        "Mean Gross FTE Salary of All Teachers (£s)",
        "Mean Gross FTE Salary of All Teachers (Â£s)",
        "Mean Gross FTE Salary of All Teachers",
        "SALARY",
    ]

### CFR DATA #################################################################
### NOT USED - REPLACED BY JOE'S DATA BELOW ##################################

cfrNames = []
cfrDict = {}
for y in ["y18"]:
    cfrNames.append(y)
    cfrDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
        "toCurr": [],
    }

cfrPaths = [r"\2017-2018\Workforce and Finance\england_cfr.csv"]
for i, name in enumerate(cfrNames):
    ad = cfrDict[name]
    ad["path"] = cfrPaths[i]
    ad["toKeep"] = cn.cfrColsToKeep
    ad["toFloat"] = ["URN", "PUPILS", "FSM"]
    ad["toPct"] = ["PTEACHINGSTAFF"]
    ad["mergeName"] = "_" + name[1:3]
    ad["toCurr"] = [
        "GRANTFUNDING",
        "TEACHINGSTAFF",
        "SELFGENERATEDINCOME",
        "SUPPLYTEACHERS",
        "EDUCATIONSUPPORTSTAFF",
        "PREMISES",
        "LEARNINGRESOURCES",
        "BOUGHTINPROFESSIONALSERVICES",
        "TOTALEXPENDITURE",
        "DCAT1",
        "DCAT2",
        "DCAT5",
    ]

### SFB Academy workforce/finance Data #######################################
### NOT USED - REPLACED BY JOE'S DATA BELOW ##################################
sfbNames = []
sfbDict = {}
for y in ["y18", "y16", "y14"]:
    sfbNames.append(y)
    sfbDict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
        "toCurr": [],
    }

sfbPaths = [
    r"\2017-2018\Workforce and Finance\SFB_Academies_2017-18_download.csv",
    r"\2015-2016\Workforce and Finance\SFR32_2017_Main_Tables.csv",
    r"\2013-2014\Workforce and Finance\SFR28_2015_Main_Tables.csv",
]
for i, name in enumerate(sfbNames):
    ad = sfbDict[name]
    ad["path"] = sfbPaths[i]
    ad["toKeep"] = cn.sfbColsToKeep
    ad["toFloat"] = ["URN", 'No Pupils','% of pupils eligible for FSM']
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]
    ad["toCurr"] = [
        'Grant Funding',
       'Self Generated Funding',
        'Teaching staff',
        'Supply teaching staff',
        'Education support staff',
        'Premises',
        'Learning resources (not ICT equipment)',
        'Brought in Professional Services',
        'Total Expenditure'
    ]

### Finance 1718 data from Joe ##################################################
#finNames = []
#finDict = {}
#for y in ["y18","y17"]:
#    finNames.append(y)
#    finDict[y] = {
#        "df": pd.DataFrame(),
#        "path": None,
#        "toKeep": [],
#        "toFloat": [],
#        "toPct": [],
#        "mergeName": None,
#        "ignore": False,
#        "stackOn": None,
#        "toCurr": [],
#    }
#
#finPaths = [
#    r"\2017-2018\Workforce and Finance\finance1718.csv",
#    r"\2016-2017\Workforce and Finance\Finance_1217.csv",
#]
#for i, name in enumerate(finNames):
#    ad = finDict[name]
#    ad["path"] = finPaths[i]
#    ad["toKeep"] =cn.finColsToKeep
#    ad["toFloat"] = ["LAESTAB"]
#    ad["toPct"] = []
#    ad["mergeName"] = "_" + name[1:3]
#    ad["toCurr"] = [x[0] for x in cn.finColsToKeep]
    




#
fin18Names = []
fin18Dict = {}
for y in ["y18"]:
    fin18Names.append(y)
    fin18Dict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
        "toCurr": [],
    }

fin18Paths = [
    r"\2017-2018\Workforce and Finance\finance1718.csv",
]
for i, name in enumerate(fin18Names):
    ad = fin18Dict[name]
    ad["path"] = fin18Paths[i]
    ad["toKeep"] = cn.fin18ColsToKeep
    ad["toFloat"] = [x[0] for x in cn.fin18ColsToKeep]
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]
    ad["toCurr"] = []
    
### Finance 1217 data from Joe ##################################################
fin17Names = []
fin17Dict = {}
for y in ["y17"]:
    fin17Names.append(y)
    fin17Dict[y] = {
        "df": pd.DataFrame(),
        "path": None,
        "toKeep": [],
        "toFloat": [],
        "toPct": [],
        "mergeName": None,
        "ignore": False,
        "stackOn": None,
        "toCurr": [],
    }

fin17Paths = [
    r"\2016-2017\Workforce and Finance\Finance_1217.csv",
]
for i, name in enumerate(fin17Names):
    ad = fin17Dict[name]
    ad["path"] = fin17Paths[i]
    ad["toKeep"] = cn.fin17ColsToKeep
    ad["toFloat"] = [x[0] for x in cn.fin17ColsToKeep]
    ad["toPct"] = []
    ad["mergeName"] = "_" + name[1:3]
    ad["toCurr"] = []
#
