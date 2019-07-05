# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:13:27 2019

@author: reesc1
"""
import pandas as pd
import re
import copy
import fullSesh

### Testing to see if stuck schools calc is working
# Starting with existing ratingsDict and checking that the predecessors are
# being calculated correctly. Seems to work - get 250 again

where = 'ONS'
if where=='ONS':
    folderPath = r"C:\Users\reesc1\Docs\Data\\"
else:
    folderPath = r"C:\Users\Chris\Documents\Documents\ONS\\"
    print('change from Academies2.xlsx to Academies.xlsx')

URNchanges = pd.read_excel(folderPath + r"\Academies2.xlsx", 
                           sheet_name='Open', skiprows=9)   

def makeTuple(row):
    return (row['URN'],row['Predecessor School URN(s)'])
URNchanges['tup'] = URNchanges.apply(makeTuple, axis=1)

URNvsPred = {}
# make dictionary of curent URN: [predecessor URN(s) list]
for URNtup in URNchanges['tup']:
    pred = URNtup[1]
    URN = int(URNtup[0])
    predList = re.findall('[0-9]{4,7}',str(pred))
    
    if len(predList) >0:
        URNvsPred[URN]=[]
        for no in predList:
            no=int(no)
            
            # Check current URN isn't listed as a predecessor
            if no==URN:
                continue
            URNvsPred[URN].append(no)

newRatingsDict = copy.deepcopy(fullSesh.copyOfRatingsDict)
newCurrentRatingsDict = copy.deepcopy(newRatingsDict)
usedCombos, notInDicts=[],[]
for URN in URNvsPred.keys():
    
    for pred in URNvsPred[URN]:
        if (URN,pred) not in usedCombos:
            usedCombos.append((URN,pred))
            try:
                if len(newRatingsDict[pred][0])>0:
                    for item in range(len(newRatingsDict[pred][0])):
                        newCurrentRatingsDict[URN][0].append(newRatingsDict[pred][0][item])
                for cat in range(1,5):
                    newCurrentRatingsDict[URN][cat] += newRatingsDict[pred][cat]
            except KeyError:
#                print('URN',URN,'pred',pred,'not in dict')
                notInDicts.append((URN,pred))
            
def stuckURN(URN, dictToUse):
    '''Looks up the given URN in the given dictionary, calculates
    whether the school is stuck and, if so, adds it to stuck list'''
    ratings = dictToUse[URN]
    if len(ratings[0]) + ratings[1] + ratings[2] + ratings[3] + ratings[4] >=4:
        if  ratings[1] + ratings[2] ==0:
            return URN
#            params['stuck'].append(URN)
#    return params['stuck']
    return None

def stuckDict(dictToUse):
    '''Applies stuckURN to each URN in the given dictionary'''
    print('Identifying stuck schools...')
    stuckList=[]
    for URN in dictToUse:
        isStuck = stuckURN(URN, dictToUse)
        if isStuck != None:
            stuckList.append(isStuck)
    print(len(stuckList),'items in stuck')
    return stuckList

stuckList = stuckDict(newCurrentRatingsDict)

if where=='ONS':
    file = 'edubaseallstatefunded20190704.csv'
else:
    file = 'edubaseallstatefunded20190627.csv'

openSchools = pd.read_csv(folderPath + file, encoding='latin-1')
openSchoolsSet = set(openSchools['URN'])

openStuckSchools = openSchoolsSet & set(stuckList)
print(len(openStuckSchools),'stuck schools from new check')







    
#    # Check oldURN is in the URN column
#    if (int(oldURN) in ratingsDict.keys()):
#        # Check not double counting as multiple rows will have same URN combo
#        if (currURN,oldURN) not in params['oldURNs']:
##            print('\ncurr',currURN,'old',oldURN)
##            print(currentRatingsDict[currURN],'+', ratingsDict[oldURN])
#            try:
#                if len(ratingsDict[oldURN][0])>0:
#                    for item in range(len(ratingsDict[oldURN][0])):
#                        currentRatingsDict[currURN][0].append(ratingsDict[oldURN][0][item])
#                for cat in range(1,5):
#                    currentRatingsDict[currURN][cat] += ratingsDict[oldURN][cat]
#            except KeyError:
#                params['subbedTheSub'].append(currURN)
#                print(currURN,'not in dict')
#    else:
#        # If previous URN is not in df0 then assume that previous URN
#        # has not been inspected since 2005 so has nothing to add
#        params['URNsNotIndf0'].append(oldURN)
