# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:10:58 2019

Sequential Forward Selection of features

@author: Chris
"""

import genericModelClass as gmc
import pandas as pd
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
import pickling
csv ='bbbbVgsbbbsWithPTRWM.csv'#:#,'bbbbVgsbbbsAllCols.csv']:#,'bbbVgsbbsLessCols.csv','bbbVgbbLessCols.csv', 'bbbbVgbbbLessCols.csv']:
df = pd.read_csv(csv)
xCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]
x = df[xCols]
y = df["Class"]

#runDict = {
#     'RF_original_260_14_entropy_False':{'clf':RandomForestClassifier(n_estimators=260, max_depth=14, criterion='entropy', bootstrap=False)},
#     'RF_original_200_15_entropy_False':{'clf':RandomForestClassifier(n_estimators=200, max_depth=15, criterion='entropy', bootstrap=False)},
#     'RF_original_180_12_entropy_False':{'clf':RandomForestClassifier(n_estimators=180, max_depth=12, criterion='entropy', bootstrap=False)},        
#     'SVM_original_2_rbf_2_0.04':{'clf':SVC(C=2, gamma=0.04)},
##       'SVM_RFE10_2_rbf_3_0.09' :{'clf':SVC(C=2, gamma=0.09)},
##       'SVM_RFE10_1.4_rbf_5_0.06':{'clf': SVC(C=1.4, gamma=0.06)},
##        'RF_OS_10_5_entropy_True':{'clf':RandomForestClassifier(n_estimators=10, max_depth=5, criterion='entropy', bootstrap=True)}
#
#     }
#
#for runName, subDict in runDict.items():
#    for forward in [True,False]:
#        featureSelector = SequentialFeatureSelector(
#         subDict['clf'],
#         k_features=(3,40),
#         forward=forward,
#         verbose=2,
#         scoring="accuracy",
#         cv=5,
#         n_jobs=-1
#         )
#        if forward:
#            subDict['Ffeatures'] = featureSelector.fit(x,y)
#            subDict['FfilteredFeatures'] = x.columns[list(subDict['Ffeatures'].k_feature_idx_)]
#        else:
#            subDict['Bfeatures'] = featureSelector.fit(x,y)
#            subDict['BfilteredFeatures'] = x.columns[list(subDict['Bfeatures'].k_feature_idx_)]
        
#print(filteredFeatures)

def showBestFeaturesOfRunDict(runDict, printOut=True, save=False):
    for runName,run in runDict.items():
        print('run name:',runName)
        for forwardsOrBackwards in ['Ffeatures','Bfeatures']:
            if save:
                saveName = runName + '_' + forwardsOrBackwards
                pickling.save_dill(run[forwardsOrBackwards].subsets_, saveName)
            numberOfFeatures = len(run[forwardsOrBackwards].k_feature_names_)
            listName = forwardsOrBackwards[0] + 'bestFeatures'
            run[listName]=[]
            if printOut:
                print(f'\n{listName} with {numberOfFeatures} features:')
                for i in run['Ffeatures'].subsets_.values():
                    for name in i['feature_names']:
                        if name not in run[listName]:
                            run[listName].append(name)
                            if printOut:
                                if len(run[listName]) < numberOfFeatures:
                                    print(i['avg_score'],name)
                if printOut:
                    print(f"------CUTOFF------ ")
          
            for i in run['Bfeatures'].subsets_.values():
                for name in i['feature_names']:
                    if name not in run[listName]:
                        run[listName].append(name)
                        if printOut:
                            if len(run[listName]) < numberOfFeatures:
                                print(i['avg_score'],name)
            
            
            
        forwardSet = set(run['Ffeatures'].k_feature_names_)
        backwardSet = set(run['Bfeatures'].k_feature_names_)
        if printOut:
            print(f"\n{runName} has {len(forwardSet)} in forwardSet, {len(backwardSet)} in backwardSet, {len(forwardSet & backwardSet)} common to both:")
            print(forwardSet & backwardSet)
    return runDict

def showBestFeaturesOfLoadedDict(loadedDict, printOut=True):
    minFeatures = min(loadedDict.keys())
    maxFeatures = max(loadedDict.keys())
    bestAvg = 0
    listOfUsedFeatures, outList = [],[]
    
    # Find best number of features
    for numOfFeatures in range(minFeatures, maxFeatures+1):
        if loadedDict[numOfFeatures]['avg_score'] > bestAvg:
            bestAvg = loadedDict[numOfFeatures]['avg_score']
            bestNumFeatures = numOfFeatures
    print('best score',bestAvg,'with',bestNumFeatures,'features')
    # Fill up list of (num, score, name) feature tuples
    for numOfFeatures in range(minFeatures, maxFeatures+1):
        currentSubDict = loadedDict[numOfFeatures]
        for feature in currentSubDict['feature_names']:
            if feature not in listOfUsedFeatures:
                outList.append((numOfFeatures, currentSubDict['avg_score'],feature))
                listOfUsedFeatures.append(feature)
#     Print out results
    for group in outList:
        if group[0] <= bestNumFeatures:
            if printOut:
                print(1,group[2])
    return outList

def processListOfPickles(listOfPickles, printOut=True):
    dictOfPickleNamesAndOutLists = {}
    for pickle in listOfPickles:    
        newDict = pickling.load_dill(pickle)
        print('\nunpacking', pickle)
        dictOfPickleNamesAndOutLists[pickle] = showBestFeaturesOfLoadedDict(newDict, printOut)
    return dictOfPickleNamesAndOutLists

def findFeatureCounts(dictOfPickleNamesAndOutLists, printOut=True):
    '''Make dict of {feature: count of feature} pairs based on appearance
    in optimum output from SFS runs in input dict'''
    counts = {}
    # Make dict with counts of each feature between runs in the input dict
    for outList in outDict.values():
        for group in outList:
            if group[2] in counts.keys():
                counts[group[2]] +=1
            else:
                counts[group[2]] = 1
    if printOut:
        featuresSoFar=0
        for count in reversed(range(len(dictOfPickleNamesAndOutLists)+1)):
            for key,val in counts.items():
                if val == count:
                    print(val, key)
                    featuresSoFar +=1
            print(featuresSoFar, 'features so far')
    return counts

def chooseColsBasedOnCount(counts, minCount):
    ''' Make a list of all of the cols that have at least the min count'''
    chosenCols = []
    for col, count in counts.items():
        if count >= minCount:
            chosenCols.append(col)
    print('\n',len(chosenCols),'cols added to chosenCols')
    return chosenCols

listOfPickles = [
                'SVM_original_2_rbf_2_0.04_Bfeatures.pik',
                'SVM_original_2_rbf_2_0.04_Ffeatures.pik',
                'RF_original_180_12_entropy_False_Bfeatures.pik',
                'RF_original_180_12_entropy_False_Ffeatures.pik',
                'RF_original_200_15_entropy_False_Bfeatures.pik',
                'RF_original_200_15_entropy_False_Ffeatures.pik',
                'RF_original_260_14_entropy_False_Bfeatures.pik',
                'RF_original_260_14_entropy_False_Ffeatures.pik']

outDict = processListOfPickles(listOfPickles)
counts = findFeatureCounts(outDict)
chosenCols = chooseColsBasedOnCount(counts, 6)

