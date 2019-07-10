# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:19:46 2019

@author: reesc1
"""

import pandas as pd
import setFolder as sf

where = sf.where
file = 'dfOnlyOpen.csv'
df0 = pd.read_csv(file)

#print(file, 'opened')
#for col in df0.columns:
#    print()
#    print(col)
#    print(df0[col].count(), 'count with', df0[col].nunique(), 'unique values')
#    if df0[col].nunique() < 15:
#        print(df0[col].value_counts())
#print('so stuck and URN are the only complete cols')
#print('add in LAESTAB col')

ebDF = pd.read_csv(sf.folderPath + sf.ebFile, encoding='latin-1')
spineDF = pd.read_csv(sf.spineFolder + r'\england_spine.csv', encoding='latin-1')

print('df0.shape',df0.shape)
df1 = df0.merge(ebDF, on='URN', how='left')       
print('df1.shape',df1.shape)
toDrop=[]
for col in ebDF.columns:
#    print()
#    print(col)
#    print(ebDF[col].count(), 'count with', ebDF[col].nunique(), 'unique values')
#    if ebDF[col].nunique() < 15:
#        print(ebDF[col].value_counts())
    if ebDF[col].count()<20000:
        toDrop.append(col)
df2 = df1.drop(toDrop, axis=1)
print('df2.shape',df2.shape)
