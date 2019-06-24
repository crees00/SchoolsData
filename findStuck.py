# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import re

global df0
folderPath = r"C:\Users\ONS_2\Documents\Chris\\" 
df0 = pd.read_csv(folderPath + 'bigDFnoDups1.csv')
print('\nData loaded!')

global ratingsDict
global currentRatingsDict
global oldURNs
global dodgyURNs
ratingsDict = {}
currentRatingsDict = {}
oldURNs, dodgyURNs = [],[]

def addRatingToDict(row):
    ''' Look up overall effectiveness rating for that row.
    Add it to the tally for that URN in the dictionary.
    If overall effectiveness is not 1-4, append it to list in position 0'''
    URN = row['URN']
    cat = row['Overall effectiveness']
    
    if URN not in ratingsDict.keys():
        ratingsDict[URN] = [[],0,0,0,0] # [random others, cat1, cat2, cat3, cat4]
    
    try:
        ratingsDict[URN][cat] += 1
    except:
        ratingsDict[URN][0].insert(0,row['Overall effectiveness'])


def addPreviousRatingsToDict(row):
    '''Look up schools/academies that are currently open. See if they have
    any predecessors and add the predecessor scores to those of the current
    school/academy.
    Dictionary contains an entry for each school/academy that is currently open
    '''
    pred = row['Predecessor School URN(s)']
    predList = re.findall('[0-9]{4,7}',str(pred))
    URN = row['URN']
    if len(predList) >0:
        for int(no) in predList:
            # Remove URN entry from dictionary
            print(no)
            try:
                currentRatingsDict.pop(no)
                print('popped')
            except:
                pass
            finally:
                
                addPredRatings(row['URN'], no)
                # Add to list of removed URNs so don't double count later
                oldURNs.append((row['URN'],no))
        

def addPredRatings(currURN, oldURN):
    '''Add the inspection ratings under the old URN to the inspection
    ratings for the current URN
    Just updates the currentRatingsDict dictionary
    '''
    print('addPredRatings',currURN,oldURN)
    if len(df0[df0['URN']==int(oldURN)])>0:
        # Check not double counting as multiple rows will have same URN combo
        if (currURN,oldURN) not in oldURNs:
            print('Add',currURN)
            currentRatingsDict[currURN][0].append(ratingsDict[oldURN][0])
            for cat in range(1,5):
                currentRatingsDict[currURN][cat] += ratingsDict[oldURN][cat]
    else:
        dodgyURNs.append(oldURN)
        print(oldURN,'Not in URN col')

df0.apply(addRatingToDict, axis=1)
currentRatingsDict = ratingsDict.copy()
df0.apply(addPreviousRatingsToDict, axis=1)
#
#110191
#118328
#106780, 137524
#106562, 106563, 134688, 138412