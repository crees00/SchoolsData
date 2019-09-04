# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:41:13 2019

@author: reesc1
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a large random dataset
rs = np.random.RandomState(33)
d = pd.read_csv('bbbbVgsbbbs6.csv')
xCols = [x for x in (set(d.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1','PTRWM_EXP__18'})]

# Compute the correlation matrix
corr = d[xCols].corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(20,20))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
hm = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#hm.get_figure().savefig('correlationMatrix.png',dpi=400)

minCorr = 0.8
colsList, scoresList = [],[]
#corrdf = pd.DataFrame({'col':None, 'row':None, 'score':None})
for col in xCols:
    for row in xCols:
        corrScore = round(corr.loc[row, col],3)
        if abs(corrScore) > minCorr:
            if row != col:
                if {row,col} not in colsList:
                    scoresList.append(corrScore)
                    colsList.append({row,col})
                    
for i, col in enumerate(colsList):
    print(scoresList[i], col)
               
                
#print(corrScore, row,' |  ', col)
        