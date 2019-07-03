# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:43:14 2019

@author: Chris
"""

import pandas as pd

##################################################################
# DOESN'T TAKE INTO ACCOUNT PREDECESSORS SO NO GOOD!!!!!!!!!!!!
##################################################################

bigdf = pd.read_csv('bigDFnoDups1.csv')
print(len(set(bigdf['URN'])),'schools to start with')
goodInspections = bigdf[bigdf['Overall effectiveness'].isin([1,2])]
goodURNs = list(set(goodInspections['URN']))

# Remove any school which has had a cat1 or cat2 inspection
print('Removing',len(goodURNs),'schools which have had a cat1 or cat2 inspection')
bigdf1s2sRemoved = bigdf[~bigdf['URN'].isin(goodURNs)]

print(len(set(bigdf1s2sRemoved['URN'])),'schools remain')
byURN = bigdf1s2sRemoved.groupby('URN')

URNsLessThan4Inspections, printCount = [],0
for URN in set(bigdf1s2sRemoved['URN']):
    if len(byURN.get_group(URN))<4:
        URNsLessThan4Inspections.append(URN)
        if printCount <10:
            print(URN)
            print(byURN.get_group(URN))
            printCount +=1
print(len(set(URNsLessThan4Inspections)),'schools in remaining df with <4 inspections')

byURNonlyenough = bigdf1s2sRemoved[~bigdf1s2sRemoved['URN'].isin(
        URNsLessThan4Inspections)]
print(len(set(byURNonlyenough['URN'])),'schools remain')

allStuckURNs = set(byURNonlyenough['URN'])   
print(len(allStuckURNs),'total stuck schools including closed')
        
openSchools = pd.read_csv('edubaseallstatefunded20190627.csv',encoding='latin-1')

openURNs = set(openSchools['URN'])
print(len(openURNs),'open schools')
openStuckURNs = allStuckURNs & openURNs
print(len(openStuckURNs),'open stuck schools')


    if len(params['bla'])<20:
        params['bla'].append('addPreviousRatingsToDict run')
