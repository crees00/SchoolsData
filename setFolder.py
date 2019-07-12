# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 13:32:43 2019

@author: reesc1
"""
where = 'ONS'
# Folder
if where=='ONS':
    folderPath = r"C:\Users\reesc1\Docs" + '\\'
else:
    folderPath = r"C:\Users\Chris\Documents\Documents\ONS\\"

# Edubase file
if where=='ONS':
    ebFile = r'Data\edubaseallstatefunded20190704.csv'
else:
    ebFile = r'edubaseallstatefunded20190627.csv'

# Spine data    
spineFolder = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\General School Information"
if where == 'ONS':
    spineFolder = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\General School Information"

# Balance data
balanceFile = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\Balance\LA_and_school_expenditure_2017-18_Tables.csv"
if where == 'ONS':
    balanceFile = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\Balance\LA_and_school_expenditure_2017-18_Tables.csv"
    
# Performance data
#perfFolder18 = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data\2017-2018\Performance"
#if where == 'ONS':
#    perfFolder18 = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\Performance"
    
    
perfFolder = r"C:\Users\Chris\Documents\Documents\ONS\DfE Data"
if where == 'ONS':
    perfFolder = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data"
