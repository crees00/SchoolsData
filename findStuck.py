# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import re

global df0
folderPath = r"C:\Users\Chris\Documents\Documents\ONS\\" 
df0 = pd.read_csv(folderPath + 'bigDFnoDups1.csv')
print('\nData loaded!')

global ratingsDict
global currentRatingsDict
global oldURNs
global URNsNotIndf0
global count
ratingsDict = {}
currentRatingsDict = {}
oldURNs, URNsNotIndf0, subbedTheSub, stuck = [],[],[],[]
count = 0

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
    if len(predList) >0:
        for no in predList:
            no=int(no)
            
            # Check current URN isn't listed as a predecessor
            if no==row['URN']:
                continue
            # Remove URN entry from dictionary as school is closed
#            print(no, 'is in Predecessor School URN(s) col for',URN)
            try:
                currentRatingsDict.pop(no)
#                print('popped')
            except:
#                print("couldn't pop - school already removed from currentRatingsDict")
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
    if currURN == oldURN:
        print('currURN == oldURN for', currURN)
        return
#    print('addPredRatings',currURN,oldURN)
    
    # Check oldURN is in the URN column
    if len(df0[df0['URN']==int(oldURN)])>0:
        # Check not double counting as multiple rows will have same URN combo
        if (currURN,oldURN) not in oldURNs:
            try:
#                print('Add',currURN)
                if len(ratingsDict[oldURN][0])>0:
                    currentRatingsDict[currURN][0].append(ratingsDict[oldURN][0])
                for cat in range(1,5):
                    currentRatingsDict[currURN][cat] += ratingsDict[oldURN][cat]
            except KeyError:
                print('KeyError. currURN =',currURN,', oldURN =',oldURN)
                subbedTheSub.append(currURN)
#                print(currURN,'not in currentRatingsDict so must be closed')
#        else:
#            print(currURN,oldURN,'already in oldURNs')
    else:
        URNsNotIndf0.append(oldURN)
#        print(oldURN,'Not in URN col')

def stuckURN(URN, count, dictToUse):
    '''Looks up the given URN in the given dictionary, calculates
    whether the school is stuck and, if so, adds it to stuck list'''
    ratings = dictToUse[URN]
    if ratings[1] + ratings[2] + ratings[3] + ratings[4] >=4:
        count += 1
        if  ratings[1] + ratings[2] ==0:
            stuck.append(URN)
            
def stuckDict(dictToUse, count):
    '''Applies stuckURN to each URN in the given dictionary'''
    for URN in dictToUse:
        stuckURN(URN, count, dictToUse)

def addStuckCol(stuck, df, write=False):
    '''Add a column called Stuck to the df
    1 if the URN is in the 'stuck' list
    0 if not stuck
    If write != False then write to .csv
    '''
    df['Stuck'] = df.apply(lambda row: np.where(
            (int(row['URN']) in stuck),1,0), axis=1)
    if write != False:
        if type(write) != str:
            raise TypeError("Need string input 'filename.csv' to addStuckCol")
        try:
            print('Writing .csv file...')
            df.to_csv(write)
        except:
            print("Couldn't write file - bad file name in addStuckCol()")

print('Filling initial dictionary...')      
df0.apply(addRatingToDict, axis=1)
print('Filled first dictionary')
currentRatingsDict = ratingsDict.copy()
print('Updating dictionary with predecessors...')
df0.apply(addPreviousRatingsToDict, axis=1)
print('Identifying stuck schools...')
stuckDict(currentRatingsDict, count)
print('Adding/updating stuck column in df...')
addStuckCol(stuck, df0, 'allDataWithStuck.csv')
print('Complete!\n')
print(len(stuck),'stuck schools')
print(len(currentRatingsDict),'open schools with an inspection since 2005')



#
#110191
#118328
#106780, 137524
#106562, 106563, 134688, 138412