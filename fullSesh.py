# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 13:03:11 2019

@author: Chris
"""
import findStuck
import pandas as pd

params = findStuck.initialiseVariables()
df0 = findStuck.loadData('bigDFnoDups1.csv')
print('Filling initial dictionary...') 

df0.apply(findStuck.addRatingToDict, axis=1, args=(params,))
params['currentRatingsDict']= params['ratingsDict'].copy()
print('Updating dictionary with predecessors...')

df0.apply(findStuck.addPreviousRatingsToDict, axis=1, args=(params,))
params['stuck'] = findStuck.stuckDict(params['ratingsDict'], params)
df0 = findStuck.addStuckCol(df0, params)
df0 = findStuck.dropCols(df0)
#df1 = findStuck.generateDFs(df0)
df2, params = findStuck.removeClosedSchools(params)
print('Complete!\n')
print(len(df2[df2['Stuck']==1]),'stuck schools')
print(len(params['openSchoolsSet']),'open schools with an inspection since 2005')


#
#allSchoolsPossible = set(allPreds) |set(ratingsDict.keys())
#print(len(allSchoolsPossible))
#set(allPreds) & set(allParents)
#allPredsSet = set(allPreds)
#openSchoolsSet = set(openSchools['URN'])
#print((allPredsSet & openSchoolsSet))
#ratingsSet = set(ratingsDict.keys())
#allStuckSet = set(stuckDict(ratingsDict,0))
#stuckSet503 = (ratingsSet - allPredsSet) & allStuckSet 
#stuckSet253 = allStuckSet & openSchoolsSet
#print(len(stuckSet253),len(stuckSet503))
#lostSchools = stuckSet503-stuckSet253
#print(len(lostSchools))
#dfnow = pd.read_csv('dfByURN.csv')
#lostSchoolsdf = dfnow[dfnow['URN'].isin(list(lostSchools))]
#lostSchoolsdf.to_csv('lostSchoolsdf.csv')