# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:23:03 2019

@author: reesc1
"""

import findStuck
import pandas as pd
import datetime
import matplotlib.pyplot as plt

params = findStuck.initialiseVariables()
params['where']='ONS'
df0 = findStuck.loadData('\code/bigDFnoDups1.csv')

#for col in df0.columns:
#    print(col, df0[col].count(), len(set(df0[col])))


cutOff = datetime.datetime(2018, 8, 31)

df0['newInspEnd'] = df0['Inspection end date'].apply(pd.to_datetime)
df8 = df0[df0['newInspEnd']<cutOff]  
df8.to_csv('bigDFnoDups1CutOffAtAug18.csv')

df9 = df0.assign(date=df0['newInspEnd']).groupby(pd.Grouper(key='newInspEnd', freq = '1M'))#.sum().reset_index()
df10= df0[['newInspEnd','Overall effectiveness']].assign(tot=df0['newInspEnd']).groupby([pd.Grouper(key='newInspEnd', freq = '1M'),'Overall effectiveness'])#.sum().reset_index()
df11 = df10.count().reset_index()
#print(df11)

print('count of each category of inspection outcome vs time (inspection start date)')
for cat in [1,2,3,4,9]:
    dfSubset = df11[df11['Overall effectiveness']==cat]
    plt.scatter(dfSubset['newInspEnd'],dfSubset['tot'], s=4)
    plt.legend()

#2018-12-19 00:00:00.000   