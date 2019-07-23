# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

@author: reesc1
"""

import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('dfForModelModified.csv')

xCols = [x for x in (set(df.columns) - {'URN','Stuck','Unnamed: 0'})]

for col in xCols:
    print('\n\n',col)
    fig = plt.figure(figsize = (10,8))
    plt.plot(df[col], marker='.', linewidth = 0, markersize = 1)

    plt.show()
    
