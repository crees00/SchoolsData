# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:00:57 2019

analyse a version of 'modelDict' which is run on just a subset of the best models

each model in modelDict will be one of 5 folds


For each model:
    find the test set
    Identify which URNs are in the test set
    Get the predictions on the training set
    make dictionary with {URN: Prediction} pairs
    
At the end of this loop:
    can save the dict and don't immediately need to keep modelDict
    merge the 5 dictionaries for each model, to have one dict for each model, containing every school in df and its prediction

Now make dict of dicts, with {runName:{URN:pred, URN:pred,...},...}
Can also make confusion matrix for each run

@author: Chris
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    roc_auc_score,
    auc,
    classification_report,
)
import re
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import RFE
import itertools
from random import sample
import datetime
import colSubsets as CS
import setFolder as sf


df = pd.read_csv(sf.addFolderPath('bbbbVgsbbbsdf7.csv'))
def makeDFofResults(write=''):
    numSchools = len(df)
    bigDF= pd.DataFrame({'tester':np.zeros(len(df))}, index=list(range(len(df))))
    oldName=''
    for modelName, modelInstance in modelDict.items():
    #    if modelName[-11:]=='_42_brute_1':
        newName = ''.join(re.split('_[0-9]of[0-9]',modelName))
        
    #        print(modelName)
        modData = modelInstance.getData()
        xTest = modData.getxTest()
        yTest = modData.getyTest()
        xTestIndices = list(xTest.index)
        clf = modelInstance.getCLF()
        y_pred = clf.predict(xTest) # numpy ndarray of 0s and 1s
        # turn array of predictions for this test set into a dataframe
        y_predDFOneRun = pd.DataFrame({newName:y_pred}, index=xTestIndices)
        
        # combine the 5 dataframes into a single one
        if oldName != newName: # First fold of this set of 5 runs
            DF5runs = y_predDFOneRun
            numOfDFsAdded = 1
        else:
            DF5runs = DF5runs.append(y_predDFOneRun)
            numOfDFsAdded += 1
        if DF5runs.shape[1]>1:
            raise 'modelDict not in order so change the way bigDF is made'
        if numOfDFsAdded ==5:
            bigDF = bigDF.join(DF5runs)
        oldName=newName       
        
        
            
    #        bigDF = bigDF.join(y_predDF)
    #        print(y_pred)        
    #        print(modelName)
    #        print(modData.getxTest().index)
    bigDF.drop('tester', axis=1, inplace=True)
    
    bigDF['TheTruth'] = df['Class'][:]
    if write != '':
        bigDF.to_csv(sf.addFolderPath(write))
    
    return bigDF

#bigDF = makeDFofResults('comparePredsdf7.csv')

def makeDFofDiffsWithTrueValues(bigDF, write=''):
    accdf = pd.DataFrame()
    for col in bigDF.columns:
        accdf[col] = bigDF[col] - bigDF['TheTruth']
    if write !='':
        accdf.to_csv(sf.addFolderPath(write))
    return accdf

bestScore=0
for col in accdf:
    if col=='TheTruth':
        continue
    runScore = accdf[col].value_counts()[0]
    if runScore>bestScore:
        bestScore = runScore
        bestRun = col
        
#bigDF = makeDFofResults('comparePredsdf7.csv')
accdf = makeDFofDiffsWithTrueValues(bigDF, 'accdfForDF7.csv')