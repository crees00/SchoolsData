# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:19:46 2019

@author: reesc1
"""

import pandas as pd
import setFolder as sf

where = sf.where

print("Opening files..")
df0 = pd.read_csv("dfOnlyOpen.csv")
ebDF = pd.read_csv(sf.folderPath + sf.ebFile, encoding="latin-1")
spineDF = pd.read_csv(sf.spineFolder + r"\england_spine.csv", encoding="latin-1")
balanceDF = pd.read_csv(sf.balanceFile, header=7, encoding="latin-1")
print("Files opened!")
# print(file, 'opened')
# for col in df0.columns:
#    print()
#    print(col)
#    print(df0[col].count(), 'count with', df0[col].nunique(), 'unique values')
#    if df0[col].nunique() < 15:
#        print(df0[col].value_counts())
# print('so stuck and URN are the only complete cols')
# print('add in LAESTAB col')


print("df0.shape", df0.shape)
print("adding edubase cols..")
df1 = df0.merge(ebDF, on="URN", how="left")
print("df1.shape", df1.shape)
toDrop = []
for col in ebDF.columns:
    if ebDF[col].count() < 20000:
        toDrop.append(col)
print("dropping cols..")
df2 = df1.drop(toDrop, axis=1)
print("df2.shape", df2.shape)

# Add LAESTAB col
print("adding LAESTAB col..")
df2["LAESTAB"] = df2.apply(
    lambda row: int(str(row["LA (code)"]) + str(row["EstablishmentNumber"])), axis=1
)
print("df2.shape", df2.shape)
print("adding balance data..")
df3 = df2.merge(
    balanceDF, left_on="LAESTAB", right_on="LA/ESTAB number", how="left", indicator=True
)
print("df3.shape", df3.shape)
