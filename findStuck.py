# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

folderPath = r"C:\Users\ONS_2\Documents\Chris\\" 
df0 = pd.read_csv(folderPath + 'bigDFnoDups1.csv')
print('Data loaded!')

global ratingsDict
ratingsDict = {}
blanks = [[],0,0,0,0] # [random others, cat1, cat2, cat3, cat4]

def addRatingToDict(row):
    ''' Look up overall effectiveness rating for that row.
    Add it to the tally for that URN in the dictionary.
    If overall effectiveness is not 1-4, append it to list in position 0'''
    URN = row['URN']
    cat = row['Overall effectiveness']
    print(URN, cat)
    
    if URN not in ratingsDict.keys():
        ratingsDict[URN] = blanks.copy()
    print(ratingsDict[URN])
    
    try:
        ratingsDict[URN][cat] += 1
    except:
        print(ratingsDict[URN])
        print(ratingsDict[URN][0])
        ratingsDict[URN][0].insert(0,cat)
        print(ratingsDict[URN][0])

    print(ratingsDict)
df0.apply(addRatingToDict, axis=1)
        