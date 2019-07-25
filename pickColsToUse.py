# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 08:20:30 2019

@author: reesc1
"""

import creatingAMonster as cam
import pandas as pd
import colNames as cn
import numpy as np

df = pd.read_csv("df5.csv")


def makePickColsToUse(df, writeName=""):
    outDF = pd.DataFrame()
    for col in df.columns:
        colType = df[col].dtype
        count = f"{df[col].count()} count"
        pctFull = f"{(100*df[col].count()/len(df))//1}% full"
        missing = f"{len(df) - df[col].count()} missing"
        unique = f"{df[col].nunique()} unique."
        valCounts = ""
        example1 = f"e.g.: {df[col].loc[df[col].first_valid_index()]}"
        example2 = df[col].iloc[1000]
        example3 = df[col].iloc[2000]
        example4 = df[col].iloc[11000]
        try:
            example5 = df[col].iloc[17000]
        except IndexError:
            example5 = ''
        describe = df[col].describe()
        if df[col].nunique() < 11:
            valCounts = df[col].value_counts()
        else:
            for line in [example1, example2, example3, example4, example5]:
                valCounts = valCounts + ("\n" + str(line))
        #    example2 = f"e.g.: {df[col].loc[df[col].second_valid_index()]}"

        outDF[col] = [colType, count, pctFull, missing, unique, describe, valCounts]
        if writeName != "":
            outDF.to_csv(writeName)
    return outDF


outDF = makePickColsToUse(df)
# outDF.to_csv('pickColsToUse.csv')

toKeep = cn.modelColsToKeep

toDrop = set(df.columns) - set(toKeep)

dfForModel = cam.dropColsFromList(df, toDrop)


def fixCategoricalCols(df):
    # 1 for boarding, 0 for not
    df["BoardingNew"] = np.where(
        df["Boarders (name)"].isin(
            [
                "Boarding school",
                "Children's home (Boarding school)",
                "College / FE residential accomodation",
            ]
        ),
        1,
        0,
    )
    # 1 for 6th form, 0 for not
    df["SixthFormNew"] = np.where(
        df["OfficialSixthForm (name)"].isin(["Has a sixth form"]), 1, 0
    )
    df["HasBoysNew"] = np.where(df["Gender (name)"].isin(["Mixed", "Boys"]), 1, 0)
    df["HasGirlsNew"] = np.where(df["Gender (name)"].isin(["Mixed", "Girls"]), 1, 0)
    df[["PNUMEAL", "PNUMFSM", "PERCTOT"]] = df[["PNUMEAL", "PNUMFSM", "PERCTOT"]].apply(
        lambda x: x / 100
    )
    df["MaintainedNew"] = np.where(df["MINORGROUP"] == "Maintained School", 1, 0)
    df["AcademyNew"] = np.where(df["MINORGROUP"] == "Academy", 1, 0)
    df["SpecialNew"] = np.where(df["MINORGROUP"] == "Special School", 1, 0)
    df = cam.dropColsFromList(
        df,
        ["Boarders (name)", "OfficialSixthForm (name)", "Gender (name)", "MINORGROUP"],
    )
    df = pd.get_dummies(df, prefix="GOR", columns=["GOR (name)"])
    return df


def normalise01Col(colOfDF):
    colMin = np.min(colOfDF)
    colMax = np.max(colOfDF)
    return (colOfDF - colMin) / (colMax - colMin)


def normaliseSDcol(colOfDF):
    return (colOfDF - (np.mean(colOfDF))) / (np.std(colOfDF))


def normalise(df, cols, func):
    for col in cols:
        df[col] = func(df[col])
    return df


toNormaliseWithStD = [
    "Mean Gross FTE Salary of All Teachers (Â£s)",
    "Total revenue balance (1) 2017-18",
    "PERCTOT",
    "TotalRevBalance Change 7yr",
    "TotalRevBalance Change 2yr",
    "Total revenue balance (1) as a % of total revenue income (6) 2017-18",
    "TotalRevBalance Change 4yr",
    "Pupil:     Teacher Ratio",
    "PSENELSE__18",
]

#dfForModelModified = fixCategoricalCols(dfForModel)
#dfForModelModified = normalise(
#    dfForModelModified,
#    [
#        x
#        for x in (
#            (set(dfForModelModified.columns) - {"URN", "GOR (name)"})
#            - set(toNormaliseWithStD)
#        )
#    ],
#    normalise01Col,
#)
#dfForModelModified = normalise(dfForModelModified, toNormaliseWithStD, normaliseSDcol)
#makePickColsToUse(dfForModel, "dfForModelAnalysed.csv")
##makePickColsToUse(dfForModelModified, "dfForModelModifiedAnalysed.csv")
#dfForModel.to_csv("dfForModel.csv")
#dfForModelModified.to_csv("dfForModelModified.csv")
