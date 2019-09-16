#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:21:37 2019

@author: reesc1
"""
import pandas as pd
import setFolder as sf
# Make lessCols list
df = pd.read_csv(sf.addFolderPath( 'bbbbVgsbbbsdf7.csv'))
final=[]
cols = list(df.columns)
for col in cols:
    if col[-5:]!='.2018':
        if col[-6:]!='yrDiff':
            final.append(col)

lessCols=['ISPRIMARY',
 'GOR_North East',
 'PTMOBN__18',
 'Unnamed: 0.1',
 'HasGirlsNew',
 'Mean Gross FTE Salary of All Teachers (Â£s)',
 'PTKS1GROUP_M__18',
 'Class',
 'BoardingNew',
 'ISPOST16',
 'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
 'GOR_West Midlands',
 'TotalRevBalance Change 7yr',
 'GOR_North West',
 'URN',
 'AGEL',
 'AcademyNew',
 'GOR_East of England',
 'GOR_East Midlands',
 'PTKS1GROUP_L__18',
 'PNUMFSM',
 'MaintainedNew',
 'Unnamed: 0',
 'Total revenue balance (1) 2017-18',
 'PSENELSE__18',
 'Pupil:     Teacher Ratio',
 'GOR_London',
 'PNUMEAL',
 'GOR_South East',
 'TotalRevBalance Change 2yr',
 'PTFSM6CLA1A__18',
 'TOTPUPS__18',
 'PerformancePctRank',
 'AGEH',
 'SixthFormNew',
 'GOR_Yorkshire and the Humber',
 'GOR_South West',
 'PERCTOT',
 'SpecialNew',
 'TotalRevBalance Change 4yr',
 'ISSECONDARY',
 'HasBoysNew',
 'PTKS1GROUP_H__18']

chosenCols1 = [ 
 'PTRWM_EXP__18',
 'PTMOBN__18',
 'SixthFormNew',
 'Total.Spend.pp_2yrDiff',
 'Mean Gross FTE Salary of All Teachers (Â£s)',
 'PTKS1GROUP_M__18',
 'GOR_East of England',
 'PERCTOT',
 'GOR_South West',
 'AGEH',
 'PSENELSE__18',
 'PNUMFSM',
 'GOR_South East',
 'Teaching.Staff.2018',
 'TotalRevBalance Change 7yr',
 'ISPRIMARY',
 'Teaching.Staff_4yrDiff',
 'Total revenue balance (1) 2017-18',
 'ISSECONDARY',
 'GOR_North East',
 'Back.Office_4yrDiff',
 'Premises_2yrDiff',
 'Other_4yrDiff',
 'Consultancy.2018',
 'Premises.2018',
 'Premises_4yrDiff',
 'Learning.Resources_4yrDiff',
 'Other.2018',
 'AcademyNew',
 'Teaching.Staff_2yrDiff',
 'BoardingNew',
 'Other.Staff_2yrDiff',
 'Back.Office_2yrDiff',
 'Ed.Support.Staff.2018',
 'ICT_2yrDiff',
 'Catering_2yrDiff',
 'Energy.2018',
 'MaintainedNew',
 'Other_2yrDiff',
 'ICT.2018',
 'Total.Income.pp_4yrDiff',
 'HasBoysNew',
 'SpecialNew',
 'HasGirlsNew',
 'GOR_London',
 'TOTPUPS__18',
 'Supply.Staff_2yrDiff',
 'Supply.Staff.2018',
 'TotalRevBalance Change 2yr',
 'ISPOST16',
 'GOR_North West']

SFS1Cols = [
'Total revenue balance (1) 2017-18',
'GOR_South West',
'ISSECONDARY',
'GOR_London',
'AcademyNew',
'SpecialNew',
'ISPRIMARY',
'HasBoysNew',
'SixthFormNew',
'BoardingNew',
'HasGirlsNew',
'MaintainedNew',
'GOR_North East',
'ISPOST16',
'GOR_East of England',
'TotalRevBalance Change 7yr',
'PTMOBN__18',
'Supply.Staff.2018',
'PTKS1GROUP_M__18',
'Supply.Staff_2yrDiff',
'Pupil:     Teacher Ratio',
'Learning.Resources_4yrDiff',
'Premises_2yrDiff',
'Premises.2018',
'Back.Office_2yrDiff',
'PTRWM_EXP__18',
'AGEH',
'PNUMFSM',
'GOR_Yorkshire and the Humber',
'Energy.2018',
'PERCTOT',
'Catering_4yrDiff',
'TOTPUPS__18',
'Premises_4yrDiff',
'Total.Income.pp_4yrDiff',
'Teaching.Staff_2yrDiff',
'GOR_North West',
'GOR_South East',
'Ed.Support.Staff.2018'
]

allCols = ['Total revenue balance (1) 2017-18',
       'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
       'TotalRevBalance Change 7yr', 'TotalRevBalance Change 4yr',
       'TotalRevBalance Change 2yr', 'TOTPUPS__18', 'PTKS1GROUP_L__18',
       'PTKS1GROUP_M__18', 'PTKS1GROUP_H__18', 'PTFSM6CLA1A__18', 'PTMOBN__18',
       'PSENELSE__18', 'PNUMEAL', 'PNUMFSM', 'PERCTOT', 'ISPRIMARY',
       'ISSECONDARY', 'ISPOST16', 'AGEL', 'AGEH', 'Pupil:     Teacher Ratio',
       'Mean Gross FTE Salary of All Teachers (Â£s)', 'BoardingNew',
       'SixthFormNew', 'HasBoysNew', 'HasGirlsNew', 'MaintainedNew',
       'AcademyNew', 'SpecialNew', 'GOR_East Midlands', 'GOR_East of England',
       'GOR_London', 'GOR_North East', 'GOR_North West',
       'GOR_South East', 'GOR_South West', 'GOR_West Midlands',
       'GOR_Yorkshire and the Humber', 'Self.Income.2018',
       'Total.Income.pp.2018', 'Teaching.Staff.2018', 'Supply.Staff.2018',
       'Ed.Support.Staff.2018', 'Premises.2018', 'Back.Office.2018',
       'Catering.2018', 'Other.Staff.2018', 'Energy.2018',
       'Learning.Resources.2018', 'ICT.2018', 'Consultancy.2018', 'Other.2018',
       'Total.Spend.pp.2018', 'PerformancePctRank', 'Self.Income_2yrDiff',
       'Self.Income_4yrDiff', 'Total.Income.pp_2yrDiff',
       'Total.Income.pp_4yrDiff', 'Teaching.Staff_2yrDiff',
       'Teaching.Staff_4yrDiff', 'Supply.Staff_2yrDiff',
       'Supply.Staff_4yrDiff', 'Ed.Support.Staff_2yrDiff',
       'Ed.Support.Staff_4yrDiff', 'Premises_2yrDiff', 'Premises_4yrDiff',
       'Back.Office_2yrDiff', 'Back.Office_4yrDiff', 'Catering_2yrDiff',
       'Catering_4yrDiff', 'Other.Staff_2yrDiff', 'Other.Staff_4yrDiff',
       'Energy_2yrDiff', 'Energy_4yrDiff', 'Learning.Resources_2yrDiff',
       'Learning.Resources_4yrDiff', 'ICT_2yrDiff', 'ICT_4yrDiff',
       'Consultancy_2yrDiff', 'Consultancy_4yrDiff', 'Other_2yrDiff',
       'Other_4yrDiff', 'Total.Spend.pp_2yrDiff', 'Total.Spend.pp_4yrDiff',
       'URN', 'Class']
############################################################################################
# From round 1 of SFS with df7
GNBcols=[
        'TotalRevBalance Change 4yr',
'Total.Income.pp.2018',
'Supply.Staff.2018',
'Total revenue balance (1) 2017-18',
'Self.Income.2018',
'Mean Gross FTE Salary of All Teachers (Â£s)',
'PSENELSE__18',
'TotalRevBalance Change 7yr',
'Ed.Support.Staff.2018',
'Consultancy_2yrDiff',
]

KNNcols1=[
'Total revenue balance (1) 2017-18',
'TotalRevBalance Change 4yr',
'HasGirlsNew',
'HasBoysNew',
'ISPRIMARY',
'Catering.2018',
'GOR_North East',
'Ed.Support.Staff_4yrDiff',
'BoardingNew',
'Back.Office_2yrDiff',
'Consultancy.2018',
'Consultancy_2yrDiff',
'SpecialNew',
'Ed.Support.Staff_2yrDiff',
'PERCTOT',
'Other.Staff_4yrDiff',
'Learning.Resources.2018',
'Other.2018',
'Other_4yrDiff',
'Energy_4yrDiff',
'TotalRevBalance Change 7yr',
'Teaching.Staff.2018',
'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
'Learning.Resources_4yrDiff',
'ISSECONDARY',
'SixthFormNew',
'ISPOST16',
'Catering_2yrDiff',
]

LRcols=[
'Total revenue balance (1) 2017-18',
'Supply.Staff_2yrDiff',
'TotalRevBalance Change 7yr',
'Other_4yrDiff',
'Teaching.Staff_4yrDiff',
'Other.Staff_4yrDiff',
'Other.Staff_2yrDiff',
'Supply.Staff.2018',
'Ed.Support.Staff.2018',
]

NNcols1=[
'Total revenue balance (1) 2017-18',
'Other.Staff_2yrDiff',
'Premises_4yrDiff',
'Mean Gross FTE Salary of All Teachers (Â£s)',
'Supply.Staff_2yrDiff',
'BoardingNew',
'TotalRevBalance Change 7yr',
'TotalRevBalance Change 2yr',
'Supply.Staff_4yrDiff',
'PNUMEAL',
'GOR_West Midlands',
'MaintainedNew',
'GOR_North East',
'ISPOST16',
'Supply.Staff.2018',
'Other.2018',
'Learning.Resources_2yrDiff',
'TotalRevBalance Change 4yr',
'ICT.2018',
]

RFcols1=[
        'TotalRevBalance Change 4yr',
'PerformancePctRank',
'Supply.Staff_4yrDiff',
'ISSECONDARY',
'TotalRevBalance Change 7yr',
'PTKS1GROUP_H__18',
'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
'AGEL',
]


SVMcols1=[
        'TotalRevBalance Change 7yr',
'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
'Supply.Staff_2yrDiff',
'Mean Gross FTE Salary of All Teachers (Â£s)',
'Consultancy_4yrDiff',
'Ed.Support.Staff_4yrDiff',
'Consultancy.2018',
]

################## SFS2 with df7 #############################################
KNNcols2=[
'TotalRevBalance Change 4yr',
'Total revenue balance (1) 2017-18',
'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
'ISSECONDARY',
'Premises_4yrDiff',
'Learning.Resources.2018',
'PerformancePctRank',
'HasGirlsNew',
'HasBoysNew',
'BoardingNew',
'Back.Office_4yrDiff',
'Consultancy.2018',
'Energy_2yrDiff',
'Energy_4yrDiff',
'Ed.Support.Staff_2yrDiff',
'Premises_2yrDiff',
'Learning.Resources_2yrDiff',
'Supply.Staff_2yrDiff',
'Catering_4yrDiff',
'SpecialNew',
'Self.Income.2018',
'MaintainedNew',
'GOR_South West',
'GOR_North East',
'ICT.2018',
'Other.2018',
'Energy.2018',
'Consultancy_4yrDiff',
]

NNcols2=[
        'TotalRevBalance Change 7yr',
'Mean Gross FTE Salary of All Teachers (Â£s)',
'Supply.Staff_2yrDiff',
'Energy_4yrDiff',
'Back.Office_2yrDiff',
'Learning.Resources.2018',
'PTFSM6CLA1A__18',
'Other.Staff_2yrDiff',
'Other_2yrDiff',
'Energy_2yrDiff',
'Total.Spend.pp_4yrDiff',
]


RFcols2=['TotalRevBalance Change 4yr',
'Teaching.Staff.2018',
'ISSECONDARY',
'GOR_North West',
'TotalRevBalance Change 7yr',
'Catering.2018',
'GOR_East Midlands',
'HasGirlsNew',
'AGEL',
'ISPRIMARY',
'Self.Income_2yrDiff',
'SpecialNew',
]

SVMcols2=['Total revenue balance (1) 2017-18',
'TotalRevBalance Change 2yr',
'Supply.Staff_2yrDiff',
'Teaching.Staff_4yrDiff',
'Ed.Support.Staff.2018',
'GOR_Yorkshire and the Humber',
'Energy.2018',
'Back.Office_4yrDiff',
'Premises_4yrDiff',
'HasBoysNew',
'Supply.Staff.2018',
'TotalRevBalance Change 7yr',
'Consultancy_2yrDiff',
'Other_2yrDiff',
'Other.Staff.2018',
'Energy_2yrDiff',
'ICT_4yrDiff',
]




#
if __name__ == "__main__":
    groupDict = {'SVMcols2':SVMcols2,'RFcols2':RFcols2,'GNBcols':GNBcols,'LRcols':LRcols,'NNcols2':NNcols2,'KNNcols2':KNNcols2}
    featureCounts={}
    import pandas as pd
    featuresDF = pd.DataFrame()
    allfeatures=set()
    for name1 in ['SVMcols2','RFcols2','GNBcols','LRcols','NNcols2','KNNcols2']:
        for feature in groupDict[name1]:
            allfeatures = allfeatures | {feature}
    allfeatures = list(allfeatures)
    df = pd.Series({feature:0 for feature in allfeatures})
    for name1 in ['SVMcols2',
                  'RFcols2',
#                  'GNBcols',
                  'LRcols',
                  'NNcols2',
                  'KNNcols2']:
        
        for feature in groupDict[name1]:
            df[feature] +=1
    df = df.sort_values(ascending=False)
#        for name2 in ['SVMcols2','RFcols2','GNBcols','LRcols','NNcols2','KNNcols2']:
#            if name1==name2:
#                continue
#            group1 = groupDict[name1]
#            group2 = groupDict[name2]
#            shared = set(group1) & set(group2)
#            just1 = set(group1) - set(group2)
#            just2 = set(group2) - set(group1)
#            print('\n\n\n\n\n',name1, name2)
#            print('shared',len(shared),'\n',shared)
#            print('\njust',name1,len(just1), '\n',just1)
#            print('\njust',name2,len(just2), '\n',just2)