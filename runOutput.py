# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:49:17 2019

@author: Chris
"""
import pandas as pd
import numpy as np
from genericModelClass import Model

def exportResultsDF(dic, write=''):
    print('saving..')
    dictToDF  ={}
    for name in dic.keys():
        mod = dic[name]
#        entry = dictToDF[name]
#        entry = {key: mod.value() for (key, value) in entryInput.items()}
        entry = {}
        for key, func in entryInput.items():
            entry[key] = func(mod)

        dictToDF[name]=entry
    outDF = pd.DataFrame(dictToDF)
    if len(write)>0:
        outDF.to_csv(write)
        print(write,'file written')
    return outDF

entryInput={
                    'acc':Model.getAcc,
                    'cm':Model.getCM,
                    'auc':Model.getAUC,
                    'cr':Model.getCR,
                    'F0':Model.getF0,
                    'F1':Model.getF1,
                    'longName':Model.getLongName,
                    'params':Model.getParams,
                    'precision0':Model.getPrecision0,
                    'precision1': Model.getPrecision1,
                    'recall0': Model.getRecall0,
                    'recall1': Model.getRecall1,
                    'runCode':Model.getRunCode,
                    'runName':Model.getRunName,
                    'tpr':Model.getTPR,
                    'fpr':Model.getFPR}

def makeAvgResults(modelDict, write=''):
    ''' For k-fold cross validation
    Makes an average of the k folds for each run setup'''
    modelScoresDict, modelAvgDict = {},{}
    # Fill up a dict of dicts with a list of scores for each run
    for run in modelDict.keys():
        loc = run.find('of')
        if loc>0:
            avgName = run[:loc-2] + run[loc+3:]
            if avgName not in modelScoresDict.keys():
                entry={}
                for key, func in entryInput.items():
#                    print(modelDict[run])
#                    print(key, func)
                    entry[key] = [func(modelDict[run])]
#                    print(entry)
#                entry = {key: [func(modelDict[run])] for (key, func) in entryInput.items()}
                modelScoresDict[avgName] = entry
            else:
                for score in modelScoresDict[avgName].keys():
#                    print(modelScoresDict[avgName])
#                    print(modelScoresDict[avgName][score])
                    scoreToAppend = entryInput[score](modelDict[run])
                    modelScoresDict[avgName][score].append(scoreToAppend)
 
    # Fill up a dict of dicts with just an average score for each set of runs
    for runName, runResultsDict in modelScoresDict.items():
        modelAvgDict[runName] = {}
        print(runResultsDict.keys())
        for score in (set(runResultsDict.keys()) - 
                      {'cr','longName','params','runCode','runName','tpr','fpr','cm'}):
            print(score)
            print(runResultsDict[score])
            print(np.mean(runResultsDict[score]))
            modelAvgDict[runName][score] = np.mean(runResultsDict[score])
            modelAvgDict[runName]['acc variance'] = np.var(runResultsDict['acc'])
    
    if len(write)>0:
        outDF = pd.DataFrame(modelAvgDict)
        outDF.to_csv(write)
        print(write,'file written')
#
    return modelAvgDict, modelScoresDict
#exportResultsDF(modelDict, 'modelDictOut1.csv')