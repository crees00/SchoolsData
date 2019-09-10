# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 13:32:43 2019

@author: reesc1
"""

where = 'laptop'


from os.path import exists

def addFolderPath(fileName, folderName=""):
    ''' put in a filename, out comes folderpath\filename
    put in a foldername and a filename, out comes folderpath\folder\filename'''
    import os
    return os.path.join(folderPath, folderName,fileName)
#def findWhere():
#    where = input('put in a where:\n')
#    return where
#
#try:
#    if not exists(spineFolder):
#        print('No folder')
#        where = findWhere()
#except NameError:
#    where = findWhere()
    
if where in ["ONS", 'Cdrive']:
    folderPath = r"C:\Users\reesc1\Docs" 
elif where in ['mac']:
    folderPath = '/Users/reesc1/Documents/personal/personal/code'
else:
    folderPath = r"C:\Users\Chris\Documents\Documents\ONS"

# Edubase file
if where in ["ONS", 'Cdrive']:
    ebFile = r"Data\edubaseallstatefunded20190704.csv"
else:
    ebFile = r"edubaseallstatefunded20190627.csv"

# Spine data
spineFolder = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\General School Information"
if where == "ONS":
    spineFolder = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\General School Information"
if where == 'Cdrive':
    spineFolder = r"C:\Users\reesc1\Docs\Data\DfE Data\2017-2018\General School Information"

# Balance data
balanceFile = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\Balance\LA_and_school_expenditure_2017-18_Tables.csv"
if where == "ONS":
    balanceFile = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\Balance\LA_and_school_expenditure_2017-18_Tables.csv"
if where == 'Cdrive':
    balanceFile = r"C:\Users\reesc1\Docs\Data\DfE Data\2017-2018\Balance\LA_and_school_expenditure_2017-18_Tables.csv"

# Performance data
# homeFolder18 = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\Performance"
# if where == 'ONS':
#    homeFolder18 = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\Performance"


homeFolder = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data"
if where == "ONS":
    homeFolder = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data"
if where == "Cdrive":
    homeFolder = r"C:\Users\reesc1\Docs\Data\DfE Data"
    
#
#if not exists(spineFolder):
#    raise FileNotFoundError