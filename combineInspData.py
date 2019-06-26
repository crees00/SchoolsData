# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:06:22 2019

@author: Chris
"""

import pandas as pd

folderPath = r"C:\Users\Chris\Documents\Documents\ONS"
fileName = folderPath + r"\Ofsted Data\Copy of Management_information_-_schools_-_1_Sept_2005_to_31_August_2015.xlsx"
df = pd.read_excel(fileName, sheet_name='2005-2015 Inspections', skiprows=0,header=1)

# Format: Filename, SheetName, skiprows, header
fileNames = {
    'Aug16' : ['Ofsted_31_August_2016.xlsx', 'D1 Sep 15 to Aug 16', None, 0],
    'Aug17' : ['Ofsted_31_August_2017.xlsx', 'D1 Sep 16 to Aug 17', None, 0],
    'Aug18' : ['Ofsted_31_August_2018.xlsx', '1 Sep 17 to 31 Aug 2018', None, 0],
    'Dec15' : ['Ofsted_31_December_2015.xlsx', 'D1 Sept to Dec 2015', None, 0],
    'Dec16' : ['Ofsted_31_December_2016.xlsx', 'D1 Sep 16 to Dec 16', None, 0],
    'Dec17' : ['Ofsted_31_December_2017.xlsx', 'D1 Sep 17 to Dec 17', None, 0],
    'Dec18' : ['Ofsted_31_December_2018.xlsx', '1 Sep 18 to 31 Dec 2018', None, 0],
    'Mar16' : ['Ofsted_31_March_2016.xlsx', 'D1 Sep 15 to Mar 16', None, 0],
    'Mar17' : ['Ofsted_31_March_2017.xlsx', 'D1 Sep 16 to Mar 17', None, 0],
    'Mar18' : ['Ofsted_31_March_2018.xlsx', '1 Sep 17 to 31 Mar 2018', None, 0]}

def appendDataFrameFromFile(df0, infoList, dropCols = False):
    '''Takes original dataframe df0 and appends a dataframe to the bottom of it
    i.e. it just adds in extra rows at the bottom.
    If dropCols is True, it will delete all of the columns apart from the four
    listed in the 'toKeep' list 
    Returns new dataframe'''
    
    fileName = folderPath + r"\Ofsted Data" + '\\' + infoList[0]
    dfToAdd = pd.read_excel(fileName, 
                       sheet_name= infoList[1], 
                       skiprows= infoList[2],
                       header= infoList[3])
   
    if dropCols == True:
        toKeep = ['URN', 'Inspection start date', 'LAESTAB','Inspection number']
        toDrop1 = list(set(dfToAdd.columns) - set(toKeep))
        dfToAdd.drop(labels=toDrop1, axis=1, inplace=True)
        toDrop2 = list(set(df0.columns) - set(toKeep))
        df0.drop(labels=toDrop2, axis=1, inplace=True)
    dfDict[infoList[0][:-5]] = dfToAdd
    
    print('Appending',infoList[0],'with shape:',dfToAdd.shape, 'to df with shape:',df0.shape)
    newDF = df0.append(dfToAdd, sort=False)
    print('Output df has shape',newDF.shape)
    
    return newDF

bigDF = df.copy()
dfDict = {'0515':bigDF}

for key in fileNames.keys():
    bigDF = appendDataFrameFromFile(bigDF, fileNames[key])

#bigDFchopped = df.copy()
#dfDictChopped = {'0515':bigDFchopped}
#
#for key in fileNames.keys():
#    bigDFchopped = appendDataFrameFromFile(bigDFchopped, fileNames[key], True)

#bigDFchopped.to_csv('bigMashchopped.csv')
#bigDF = pd.read_csv('bigMash1.csv')
    
bigDFsorted = bigDF.sort_values(by = ['URN','Inspection start date'], axis=0)
bigDFnoDups = bigDFsorted.drop_duplicates('Inspection number')
print(bigDFnoDups.shape)   
 
URNchanges = pd.read_excel(folderPath + r"\Academies.xlsx", 
                           sheet_name='Open', skiprows=9)   

# Add cols showing URN of predecessor school(s)

toKeep = ['Academy Name','Open','Predecessor School URN(s)','URN']
toDrop = set(URNchanges.columns) - set(toKeep)
bigDFnoDups1 = bigDFnoDups.merge(URNchanges, how='left', on='URN', indicator=True)
bigDFnoDups1.drop(toDrop, axis=1, inplace=True)
bigDFnoDups1.to_csv('bigDFnoDups1.csv')

