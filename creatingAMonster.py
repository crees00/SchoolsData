# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:19:46 2019

@author: reesc1
"""

import pandas as pd
import numpy as np
import setFolder as sf
import re
import colNames as cn
import datetime
where = sf.where
start = datetime.datetime.now()
print(f'running creatingAMonster at {start}')
# Read in files
def readFiles():
    print("Opening files..")
    df0 = pd.read_csv("dfOnlyOpen.csv")
    ebDF = pd.read_csv(sf.folderPath + sf.ebFile, encoding="latin-1")
    spineDF = pd.read_csv(sf.spineFolder + r"\england_spine.csv", encoding="latin-1")
    try:
        balanceDF = pd.read_csv(
            sf.balanceFile, header=7, encoding="latin-1", skipfooter=8
        )
    except FileNotFoundError:
        print("File not found:", sf.balanceFile, "\nmoving on without it..")
    print("Finished reading files")
    return df0, ebDF, spineDF, balanceDF


def analyseCols(df, name=""):
    print("\n")
    print("analyseCols(", name, ")", sep="")
    scoreDict = {"blank": [], "<10%": [], "90%+": [], "99%+": [], "full": []}
    for col in df.columns:
        print()
        print(f"{col}  (type: {df[col].dtype})")
        print(
            f"{df[col].count()} ({(100*df[col].count()/len(df))//1}%) count, {len(df) - df[col].count()} missing, {df[col].nunique()} unique."
        )
        if df[col].nunique() < 15:
            print(df[col].value_counts())
        else:
            print(f"e.g.: {df[col].loc[df[col].first_valid_index()]}")
        num = df[col].count()
        if num == 0:
            scoreDict["blank"].append(col)
        if (num / len(df)) < 0.1:
            scoreDict["<10%"].append(col)
        elif (num / len(df)) > 0.9:
            scoreDict["90%+"].append(col)
            if (num / len(df)) > 0.99:
                scoreDict["99%+"].append(col)
                if (num / len(df)) > 0.99999999:
                    scoreDict["full"].append(col)
    print("\n\nSummary:\n")
    print(f"{len(df.columns)} cols, {len(df)} rows")
    for key in scoreDict.keys():
        print(f"{len(scoreDict[key])} cols {key}")


def dropColsFromList(df, toDrop):
    """ Takes each column name in toDrop and drops that col from df.
    Works regardless of whether col name from toDrop is in df"""
    try:
        return df.drop(toDrop, axis=1)
    except KeyError as error:
        colToChop = re.findall("'[\w ]+'", str(error))
        colToChop = [x[1:-1] for x in colToChop]
        toDrop = list(set(toDrop) - set(colToChop))
        return dropColsFromList(df, toDrop)


def absChange(row, col1, col2):
    """ Absolute change from col1 to col2"""
    return row[col2] - row[col1]


def pctChange(row, col1, col2):
    """ Percentage change from col1 to col2"""
    try:
        return (row[col2] - row[col1]) / row[col1]
    except ZeroDivisionError:
        return np.nan


def addCol(df, col1, col2, func):
    """ returns a new col to add to df"""
    return df.apply(func, args=((col1, col2)), axis=1)


def p2f(x):
    """converts string percentage e.g. '56%'
    to float e.g. 0.56 """
    if x != x:
        return x
    else:
        try:
            return float(x.strip("%")) / 100
        # some random text in the data so just delete it
        except ValueError:
            return np.nan

def c2f(x):
    """ converts currency string e.g. £4,122,222.01
    to float e.g. 4122222.01 """
    if x!=x:
        return x
    else:
        try:
            return float(re.sub(r'[^\d.]',"",x))
        except ValueError:
            return np.nan

# Add edubase cols
def addEdubaseCols(df0, ebDF):
    print("df0.shape", df0.shape)
    print("adding edubase cols..")
    df1 = df0.merge(ebDF, on="URN", how="left")
    print("df1.shape", df1.shape)
    toDrop = []
    for col in ebDF.columns:
        if ebDF[col].count() < 20000:
            toDrop.append(col)
    print("dropping cols..")
    df2 = dropColsFromList(df1, toDrop)
    print("df2.shape", df2.shape)

    # Add LAESTAB col
    print("adding LAESTAB col..")
    df2["LAESTAB"] = df2.apply(
        lambda row: int(str(row["LA (code)"]) + str(row["EstablishmentNumber"])), axis=1
    )
    print("df2.shape", df2.shape)
    return df2


# Update balance cols
def updateBalanceCols(balanceDF):
    """ Updates the cols in balanceDF """
    print("adding balance calc cols to balanceDF..")
    # remove '..'s
    balanceDF.replace({"..": np.nan}, inplace=True)
    # change col types
    for col in balanceDF.columns:
        if not any([("Gov" in col), ("Name" in col), ("Phase" in col)]):
            balanceDF[col] = balanceDF[col].astype(float)
    # Add new cols
    balanceDF["TotalRevBalance Change 7yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2010-11",
        "Total revenue balance (1) 2017-18",
        absChange,
    )
    balanceDF["TotalRevBalance Change 4yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2013-14",
        "Total revenue balance (1) 2017-18",
        absChange,
    )
    balanceDF["TotalRevBalance Change 2yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2015-16",
        "Total revenue balance (1) 2017-18",
        absChange,
    )
    balanceDF["PctRevBalance Change 7yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2010-11",
        "Total revenue balance (1) 2017-18",
        pctChange,
    )
    balanceDF["PctRevBalance Change 4yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2013-14",
        "Total revenue balance (1) 2017-18",
        pctChange,
    )
    balanceDF["PctRevBalance Change 2yr"] = addCol(
        balanceDF,
        "Total revenue balance (1) 2015-16",
        "Total revenue balance (1) 2017-18",
        pctChange,
    )
    return balanceDF


# Add balance data
def addBalanceData(balanceDF, df2):
    """ adds balanceDF to main df  """
    print("adding balance data..")
    try:
        df3 = df2.merge(
            balanceDF,
            left_on="LAESTAB",
            right_on="LA/ESTAB number",
            how="left",
            indicator=True,
        )
    except NameError:
        print("balanceDF not defined - not adding")
        df3 = df2
    print("df3.shape", df3.shape)
    return df3


def runAll(write=False):
    df0, ebDF, spineDF, balanceDF = readFiles()
    df2 = addEdubaseCols(df0, ebDF)
    balanceDF = updateBalanceCols(balanceDF)
    df3 = addBalanceData(balanceDF, df2)
    df4 = dropColsFromList(
        df3,
        [
            "SchoolWebsite",
            "TelephoneNum",
            "HeadTitle (name)",
            "HeadFirstName",
            "HeadLastName",
        ],
    )
    print("df4.shape", df4.shape)
    if write:
        df4.to_csv('df4.csv')
    return ebDF, spineDF, balanceDF, df0, df2, df3, df4


#ebDF, spineDF, balanceDF, df0, df2, df3, df4 = runAll(True)
print(f'monster created - took {datetime.datetime.now()-start}')