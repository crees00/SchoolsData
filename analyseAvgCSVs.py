# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:20:46 2019

@author: Chris
"""

import pandas as pd

lessCols = pd.read_csv('AVG26_8_119bbbbVgsbbbsLessCols.csv')
allCols = pd.read_csv('AVG26_8_757bbbbVgsbbbsAllCols.csv')

allCols.set_index('Unnamed: 0', inplace=True)
lessCols.set_index('Unnamed: 0', inplace=True)

allColsSorted = allCols.sort_values(by='acc', axis=1, ascending=False)
lessColsSorted = lessCols.sort_values(by='acc', axis=1, ascending=False)

print('Best accuracy:')
print('allCols',allCols.loc['acc'].max(),'for',allCols.loc['acc'].idxmax())
print('lessCols', lessCols.loc['acc'].max(),'for',lessCols.loc['acc'].idxmax())