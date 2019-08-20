# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:49:17 2019

@author: Chris
"""
import pandas as pd

def exportResultsDF(dic, write=''):
    print('saving..')
    dictToDF  ={}
    for name in dic.keys():
        mod = dic[name]
#        entry = dictToDF[name]
        entry={
                'acc':mod.getAcc(),
                'cm': mod.getCM(),
                'auc':mod.getAUC(),
                'cr':mod.getCR(),
                'F0':mod.getF0(),
                'F1':mod.getF1(),
                'longName':mod.getLongName(),
                'params':mod.getParams(),
                'precision0':mod.getPrecision0(),
                'precision1': mod.getPrecision1(),
                'recall0': mod.getRecall0(),
                'recall1': mod.getRecall1(),
                'runCode':mod.getRunCode(),
                'runName':mod.getRunName(),
                'tpr':mod.getTPR(),
                'fpr':mod.getFPR()}
        dictToDF[name]=entry
    outDF = pd.DataFrame(dictToDF)
    if len(write)>0:
        outDF.to_csv(write)
        print(write,'file written')
    return outDF


#exportResultsDF(modelDict, 'modelDictOut1.csv')