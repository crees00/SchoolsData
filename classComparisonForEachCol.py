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
import setFolder as sf
#df = pd.read_csv(sf.addFolderPath( 'notNormedForFeaturePlots_bbbbVgsbbbs.csv'))
df = pd.read_csv(sf.addFolderPath( 'AllDatanotNormedForFeaturePlots_bbbbVgsbbbs.csv'))
plotCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]

plotCols=['PNUMFSM', 'Total revenue balance (1) as a % of total revenue income (6) 2017-18','ISPRIMARY', 'Premises.2018', 'PTKS1GROUP_L__18', 'PNUMEAL','ISSECONDARY','PERCTOT','AcademyNew', 'Pupil:     Teacher Ratio','Supply.Staff_4yrDiff', 'Mean Gross FTE Salary of All Teachers (Â£s)','TOTPUPS__18', 'PerformancePctRank','AGEL']
plt.figure(figsize=(16,20))
i=0
for col in plotCols:
    i+=1
    dfB = df[df['Class']==1]
    dfG = df[df['Class']==0]
    dfO = df[df['Class']==2]
    print(col)
#    n, bins, patches = plt.hist(dfB[col], bins=30, alpha=1, density=True, label='Stuck')
#    plt.hist(dfG[col], bins=bins, alpha=0.6, density=True, label='Escaped')
    plt.subplot(5,3,i)
    n, bins, patches = plt.hist(dfO[col], bins=50, alpha=1, density=True,
                                label='Other', color='k', histtype='step')
    plt.hist(dfB[col], bins=bins, alpha=0.8, density=True, label='Stuck')
    plt.hist(dfG[col], bins=bins, alpha=0.6, density=True, label='Escaped')


#    plt.hist((dfB[col],dfG[col],dfO[col]), bins=30, density=True)
    plt.legend()
    plt.title(col )
#    plt.show()