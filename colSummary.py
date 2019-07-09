# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:19:06 2019

@author: reesc1
"""

import pandas as pd
file = 'dfOnlyOpen.csv'
dfOnlyOpen = pd.read_csv('dfOnlyOpen.csv')

print(file,'opened')
for col in dfOnlyOpen.columns:
    print()
    print(col)
    print(dfOnlyOpen[col].count(),'count with',dfOnlyOpen[col].nunique(),'unique values')
    if dfOnlyOpen[col].nunique() < 15:
        print(dfOnlyOpen[col].value_counts())