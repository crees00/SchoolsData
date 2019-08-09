# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:34:10 2019

@author: reesc1
"""

import numpy as np
import pandas as pd
import matplotlib
import missingno as msno
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

file = 'dfForModelModified.csv'
train_df = dfForModelModified#pd.read_csv(file)
originalCols = train_df.columns
print(len(originalCols))
missingdata_df = train_df.columns[train_df.isnull().any()].tolist()
msno.matrix(train_df[missingdata_df])
msno.bar(train_df[missingdata_df], color="blue", log=True, figsize=(30,18))
msno.heatmap(train_df[missingdata_df], figsize=(20,20))

#imp = IterativeImputer(max_iter=10, random_state=0)
#imp.fit(train_df)
#
#fixed_df = pd.DataFrame(imp.transform(train_df), columns=originalCols)
#
#fixed_df.to_csv(file[:-4]+'Imputed.csv')