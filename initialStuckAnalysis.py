# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:47:58 2019

@author: Chris
"""

import pandas as pd

folderPath = r"C:\Users\Chris\Documents\Documents\ONS\\"
fileName = folderPath + "dfByURN.csv"
df = pd.read_csv(fileName)
stuckdf = df[df['Stuck']==1]
blanks = pd.read_csv(folderPath+'showBlanks.csv')

for col in stuckdf.columns:
#    if len(set(stuckdf[col]))<20:
#        print(stuckdf[col].value_counts())
#        print(stuckdf[col].count(), col)
        print(df[col].count(),col)
        print(blanks[col].value_counts(),col)
        print()
        


fromCIreport = '''
490 stuck schools
290 primary
190 secondary
10 PRUs & special schools

80% of them have moved between cat3 and cat4

% FSM pupils well above national average
% white british FSM pupils well above national average
'''
