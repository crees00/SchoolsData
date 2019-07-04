# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 13:03:11 2019

@author: Chris
"""
import findStuck
import pandas as pd
#import sys
#
#orig_stdout = sys.stdout
#f = open('out.txt', 'w')
#sys.stdout = f




params = findStuck.initialiseVariables()
params['where']='ONS'
df0 = findStuck.loadData('\code/bigDFnoDups1CutOffAtAug18.csv')
print('Filling initial dictionary...') 

print('ratingsDict')
findStuck.countRatings(params['ratingsDict'])
print('currentRatingsDict')
findStuck.countRatings(params['currentRatingsDict'])
df0.apply(findStuck.addRatingToDict, axis=1, args=(params,))

print('ratingsDict')
findStuck.countRatings(params['ratingsDict'])
print('currentRatingsDict')
findStuck.countRatings(params['currentRatingsDict'])
print('\ncopying dictionary')
params['currentRatingsDict']= params['ratingsDict'].copy()
params['ratingsDict'][199999] = [[9],1,1,1,1]
print('added in something to ratingsDict')

print('ratingsDict')
findStuck.countRatings(params['ratingsDict'])
print('currentRatingsDict')
findStuck.countRatings(params['currentRatingsDict'])

print('\nUpdating dictionary with predecessors...')
df0.apply(findStuck.addPreviousRatingsToDict, axis=1, args=(params,))
print('ratingsDict')
findStuck.countRatings(params['ratingsDict'])
print('currentRatingsDict')
findStuck.countRatings(params['currentRatingsDict'])

#params['stuck'] = findStuck.stuckDict(params['currentRatingsDict'], params)
#df0 = findStuck.addStuckCol(df0, params, write=True)
#df0 = findStuck.dropCols(df0)
#df1 = findStuck.generateDFs(df0, write=True)
#df2, params = findStuck.removeClosedSchools(params,df1, write=True)
#print('Complete!\n')
#print(len(df2[df2['Stuck']==1]),'stuck schools in final df')
#print(len(params['openStuck']),'stuck schools from URN sets')
#print(len(params['openSchoolsSet']),'open schools with an inspection since 2005')


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



#sys.stdout = orig_stdout
#f.close()