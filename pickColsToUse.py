# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 08:20:30 2019

@author: reesc1
"""

import creatingAMonster as cam
import pandas as pd
import colNames as cn

df = pd.read_csv('df5.csv')
outDF = pd.DataFrame()

for col in df.columns:
    colType = df[col].dtype
    count = f"{df[col].count()} count"
    pctFull = f"{(100*df[col].count()/len(df))//1}% full"
    missing = f"{len(df) - df[col].count()} missing"
    unique = f"{df[col].nunique()} unique."
    example1 =f"e.g.: {df[col].loc[df[col].first_valid_index()]}"
    example2 = df[col].iloc[1000]
    example3 = df[col].iloc[2000]
    example4 = df[col].iloc[11000]
    example5 = df[col].iloc[17000]
    describe = df[col].describe()
#    example2 = f"e.g.: {df[col].loc[df[col].second_valid_index()]}"
    
    outDF[col] = [colType, count, pctFull, missing, unique, describe,example1,example2,example3,example4,example5]
    
outDF.to_csv('pickColsToUse.csv')

toKeep = cn.modelColsToKeep

toDrop = set(df.columns) - set(toKeep)

dfForModel = cam.dropColsFromList(df,toDrop)

dfForModel.to_csv('dfForModel.csv')