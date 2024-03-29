# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 13:03:11 2019

data in: bigDFnoDups1.csv from combineInspData.py
data out: dfOnlyOpen.csv to creatingAMonster.py

@author: Chris
"""
import findStuck
import pandas as pd
import copy
import datetime
import combineInspData

#import sys
#
#orig_stdout = sys.stdout
#f = open('analyseDF10.txt', 'w')
#sys.stdout = f

start = datetime.datetime.now()
params = findStuck.initialiseVariables()
df0 = findStuck.loadData("bigDFnoDups1.csv")
print(df0.shape)
print("Filling initial dictionary...")

print("ratingsDict", findStuck.countRatings(params["ratingsDict"]))
print("currentRatingsDict", findStuck.countRatings(params["currentRatingsDict"]))

df0 = findStuck.fixForDodgyData(df0)

df0.apply(findStuck.addRatingToDict, axis=1, args=(params,))

print("ratingsDict", findStuck.countRatings(params["ratingsDict"]))
print("currentRatingsDict", findStuck.countRatings(params["currentRatingsDict"]))

print("\ncopying dictionary")
params["currentRatingsDict"] = copy.deepcopy(params["ratingsDict"])
copyOfRatingsDict = copy.deepcopy(params["ratingsDict"])

print("ratingsDict", findStuck.countRatings(params["ratingsDict"]))
print("currentRatingsDict", findStuck.countRatings(params["currentRatingsDict"]))
print("length of ratingsDict", len(params["ratingsDict"]))
print("\nUpdating dictionary with predecessors...")
df0.apply(findStuck.addPreviousRatingsToDict, axis=1, args=(params,))
print("ratingsDict", findStuck.countRatings(params["ratingsDict"]))
print("currentRatingsDict", findStuck.countRatings(params["currentRatingsDict"]))

params["stuck"] = findStuck.stuckDict(params["currentRatingsDict"], params)

df0 = findStuck.addStuckCol(df0, params, write=True)
df0 = findStuck.dropCols(df0)
df1 = findStuck.generateDFs(df0, write=True)
df2, params = findStuck.removeClosedSchools(params, df1, write=True)
print("Complete!\n")
print(len(df2[df2["Stuck"] == 1]), "stuck schools in final df")
print(len(df2), "schools in final df")
print(len(params["openStuck"]), "stuck schools from URN sets")
print(len((params["openSchoolsSet"]) & set(df2["URN"])), "open schools in final df")
print(
    "URNs in both allParents and allPreds:",
    set(params["allParents"]) & set(params["allPreds"]),
)
print(f'fullSesh complete - took {datetime.datetime.now()-start}')
#
# allSchoolsPossible = set(allPreds) |set(ratingsDict.keys())
# print(len(allSchoolsPossible))
# set(allPreds) & set(allParents)
# allPredsSet = set(allPreds)
# openSchoolsSet = set(openSchools['URN'])
# print((allPredsSet & openSchoolsSet))
# ratingsSet = set(ratingsDict.keys())
# allStuckSet = set(stuckDict(ratingsDict,0))
# stuckSet503 = (ratingsSet - allPredsSet) & allStuckSet
# stuckSet253 = allStuckSet & openSchoolsSet
# print(len(stuckSet253),len(stuckSet503))
# lostSchools = stuckSet503-stuckSet253
# print(len(lostSchools))
# dfnow = pd.read_csv('dfByURN.csv')
# lostSchoolsdf = dfnow[dfnow['URN'].isin(list(lostSchools))]
# lostSchoolsdf.to_csv('lostSchoolsdf.csv')


#sys.stdout = orig_stdout
#f.close()
