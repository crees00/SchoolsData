# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 13:32:43 2019

@author: reesc1
"""
def setWhere(where='ONS'):
    return where
where = setWhere()

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
spineFolder = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data\2017-2018\General School Information"
