# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:10:58 2019

Sequential Forward Selection of features

@author: Chris
"""
import setFolder as sf
import genericModelClass as gmc
import pandas as pd
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import pickling
import os
csv =sf.addFolderPath('bbbbVgsbbbsdf7.csv')#:#,'bbbbVgsbbbsAllCols.csv']:#,'bbbVgsbbsLessCols.csv','bbbVgbbLessCols.csv', 'bbbbVgbbbLessCols.csv']:
df = pd.read_csv(csv)
xCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]
x = df[xCols]
y = df["Class"]

runDict = {
#             'SVM_original_3.6_rbf_2_0.005':{'clf':SVC(C=3.6, gamma=0.005)},
#        'NN_original_1_1_lbfgs_0.001':{'clf':MLPClassifier(hidden_layer_sizes=(1,), solver='lbfgs', max_iter=1000)},
#        'LR_original':{'clf':LogisticRegression(solver='lbfgs', max_iter=10000)},
#        'GNB_original':{'clf':GaussianNB()},
#     'RF_original_100_10_entropy_True':{'clf':RandomForestClassifier(n_estimators=100, max_depth=10, criterion='entropy', bootstrap=True)},
        'KNN_original_18_auto_1':{'clf':KNeighborsClassifier(n_neighbors=18, algorithm='auto', p=1)},

#        'GNB_original':{'clf':GaussianNB()},
#        'KNN_original_20_brute_3':{'clf':KNeighborsClassifier(n_neighbors=20, algorithm='brute', p=3)},
#        'LR_original':{'clf':LogisticRegression(solver='lbfgs', max_iter=10000)},
#        'NN_original_4_5_adam_0.01':{'clf':MLPClassifier(hidden_layer_sizes=(5,5,5,5), solver='adam', max_iter=1000)}
#     'RF_original_204_16_entropy_False':{'clf':RandomForestClassifier(n_estimators=204, max_depth=16, criterion='entropy', bootstrap=False)},
#     'RF_original_242_16_entropy_False':{'clf':RandomForestClassifier(n_estimators=242, max_depth=16, criterion='entropy', bootstrap=False)},
#     'RF_original_174_16_entropy_False':{'clf':RandomForestClassifier(n_estimators=174, max_depth=16, criterion='entropy', bootstrap=False)},        
#     'SVM_original_2_rbf_2_0.04':{'clf':SVC(C=2, gamma=0.04)},
##       'SVM_RFE10_2_rbf_3_0.09' :{'clf':SVC(C=2, gamma=0.09)},
##       'SVM_RFE10_1.4_rbf_5_0.06':{'clf': SVC(C=1.4, gamma=0.06)},
##        'RF_OS_10_5_entropy_True':{'clf':RandomForestClassifier(n_estimators=10, max_depth=5, criterion='entropy', bootstrap=True)}
#
     }
#
def doSFS(runDict, save=True):
    for runName, subDict in runDict.items():
        for forward in [True,False]:
            print(runName, forward)
            featureSelector = SequentialFeatureSelector(
             subDict['clf'],
             k_features=(1,50),
             forward=forward,
             verbose=2,
             scoring="accuracy",
             cv=5,
             n_jobs=-1
             )
            if forward:
                subDict['Ffeatures'] = featureSelector.fit(x,y)
                subDict['FfilteredFeatures'] = x.columns[list(subDict['Ffeatures'].k_feature_idx_)]
            else:
                subDict['Bfeatures'] = featureSelector.fit(x,y)
                subDict['BfilteredFeatures'] = x.columns[list(subDict['Bfeatures'].k_feature_idx_)]
            if save:
                forwardsOrBackwards = 'Bfeatures'
                if forward:
                    forwardsOrBackwards = 'Ffeatures'
                saveName = runName + '_' + forwardsOrBackwards
                pickling.save_dill(subDict[forwardsOrBackwards].subsets_, saveName)
    return runDict
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
    ''' Process the dict for a single run (forwards or backwards) 
    Fed by processListOfPickles'''
    minFeatures = min(loadedDict.keys())
    maxFeatures = max(loadedDict.keys())
    bestAvg = 0
    listOfUsedFeatures, outList = [],[]
    # Do initial bit for first few features because it starts at e.g. 3
    # Only for backwards as forwards has minFeatures=1
    for numFeatures in range(1,minFeatures):
        outList.append((numFeatures, 
                        loadedDict[minFeatures]['avg_score'],
                        loadedDict[minFeatures]['feature_names'][numFeatures-1]
                        ))
        listOfUsedFeatures.append(loadedDict[minFeatures]['feature_names'][numFeatures-1])
#        outList.append((numFeatures,loadedDict)
    # Find best number of features
    for numOfFeatures in range(minFeatures, maxFeatures+1):
        if loadedDict[numOfFeatures]['avg_score'] >= bestAvg:
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
                print((group[2],))
    return outList

def processListOfPickles(listOfPickles, folderName='',printOut=True):
    ''' Feeds to showBestFeaturesOfLoadedDict '''
    folderName = sf.addFolderPath(folderName)
    dictOfPickleNamesAndOutLists = {}
    for pickle in listOfPickles:  
        print(os.path.join(folderName, pickle))
        newDict = pickling.load_dill(os.path.join(folderName, pickle))
        print('\nunpacking', pickle)
        dictOfPickleNamesAndOutLists[pickle] = showBestFeaturesOfLoadedDict(newDict, printOut)
    if printOut:
        bestAcc, numFeatures, bestRun = 0,0, ''
        for runName, outList in dictOfPickleNamesAndOutLists.items():
            for group in outList:
                if group[1] > bestAcc:
                    bestAcc = group[1]
                    numFeatures = group[0]
                    bestRun = runName
        print('\nBest Results:')
        print('best accuracy, num features, best run')
        print(bestAcc, numFeatures, bestRun)
        print()
    return dictOfPickleNamesAndOutLists

def findFeatureCounts(dictOfPickleNamesAndOutLists, printOut=True):
    '''Make dict of {feature: count of feature} pairs based on appearance
    in optimum output from SFS runs in input dict'''
    counts = {}
    # Make dict with counts of each feature between runs in the input dict
    for outList in dictOfPickleNamesAndOutLists.values():
        # Find optimum number of features for that run first
        maxAcc, numFeatures = 0,0
        for group in outList:
            if group[1] > maxAcc:
                maxAcc = group[1]
                numFeatures = group[0]
        # Do the counts, just for features in optimum group for run
        for group in outList:
            if group[0] <= numFeatures:
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
            print('---',featuresSoFar, 'features so far ---')
    return counts

def chooseColsBasedOnCount(counts, minCount):
    ''' Make a list of all of the cols that have at least the min count'''
    chosenCols = []
    for col, count in counts.items():
        if count >= minCount:
            chosenCols.append(col)
    print('\n',len(chosenCols),'cols added to chosenCols')
    return chosenCols

def findFeatureAccuracy(dictOfPickleNamesAndOutLists, printOut=True):
    # Find best group of features and best score for each run
    results={}
    for runName, outList in dictOfPickleNamesAndOutLists.items():
        results[runName] = {'features':[],'score':0, 'numFeatures':0}
        # Find best score for run
        for group in outList:
            if group[1] > results[runName]['score']:
                results[runName]['score'] = group[1]
                results[runName]['numFeatures'] = group[0]
        # Find list of features for best score
        for group in outList:
            if group[0] <= results[runName]['numFeatures']:
                results[runName]['features'].append(group[2])
    
    # Combine results from all runs into one
    featureDict = {} # {'featureName':BestScoreForFeature}
    for runName, subDict in results.items():
        for feature in subDict['features']:
            if feature in featureDict.keys():
                if subDict['score'] > featureDict[feature]:
                    featureDict[feature] = subDict['score']
            else:
                featureDict[feature] = subDict['score']
    acc=1
    while acc > 0:
        for feature in featureDict.keys():
            score = featureDict[feature]
            if round(score,3) == round(acc,3):
                print((feature,))
        acc -= 1e-3
            

#listOfPickles = [
#                'SVM_original_2_rbf_2_0.04_Bfeatures.pik',
#                'SVM_original_2_rbf_2_0.04_Ffeatures.pik',
#                'RF_original_180_12_entropy_False_Bfeatures.pik',
#                'RF_original_180_12_entropy_False_Ffeatures.pik',
#                'RF_original_200_15_entropy_False_Bfeatures.pik',
#                'RF_original_200_15_entropy_False_Ffeatures.pik',
#                'RF_original_260_14_entropy_False_Bfeatures.pik',
#                'RF_original_260_14_entropy_False_Ffeatures.pik']
#
folderName = r"putthefolderhre"
#listOfPickles2 = os.listdir(sf.addFolderPath(folderName))
##
#outDict = processListOfPickles(listOfPickles2, folderName)
#counts = findFeatureCounts(outDict)
#chosenCols = chooseColsBasedOnCount(counts, 6)
#findFeatureAccuracy(outDict)
runDict = doSFS(runDict)
#showBestFeaturesOfRunDict(runDict, printOut=True, save=False)