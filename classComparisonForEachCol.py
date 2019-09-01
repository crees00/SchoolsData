# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:10:27 2019

Plot histograms of each variable with class1 vs class0
Class1 (bad next) is blue
Class0 (good next) is orange

@author: Chris
"""
from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('bbbbVgsbbbsWithPTRWM.csv')
plotCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]


for col in plotCols:
    dfG = df[df['Class']==1]
    dfB = df[df['Class']==0]
    print(col)
    n, bins, patches = plt.hist(dfG[col], bins=30, alpha=1, density=True)
    plt.hist(dfB[col], bins=bins, alpha=0.6, density=True)
    plt.show()