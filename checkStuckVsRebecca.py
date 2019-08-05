# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:35:40 2019

@author: reesc1
"""

import pandas as pd
import numpy as np

rebData = pd.read_csv('6.Groups.csv')
rebStuck = rebData[rebData['StuckFlag']==1]

# Check if school is in dict
for URN in rebStuck['URN']:
    if URN not in SchoolDict.keys():
        print (URN)
print('shown schools not in SchoolDict')

rebStuckClosed =[]
for URN in rebStuck['URN']:
    if SchoolDict[URN].getStatus() == 'closed':
        rebStuckClosed.append(SchoolDict[URN])