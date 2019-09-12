# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 15:57:56 2019

@author: Chris
"""


import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from os import listdir
import setFolder as sf


def paramHistograms(df, minAcc=0.60, minProportion=-1):
    ''' If a minProportion is set to e.g. 0.1 then accurateSubset for that
    model will be the most accurate 10% of runs for that model.
    If no minProportion set, uses minAcc set or minAcc default
    '''
    assert 'OS' in df.columns, 'needs to be df with OS, p1 etc cols added'
    for model in ['NN','RF','SVM','KNN']:
        print('\nModel:',model)
        modelSubset = df[df[model]==1]
        
        if minProportion > 0:
            minAcc=1
        
        accurateSubset = modelSubset[modelSubset['acc']>minAcc]
        
        while (len(accurateSubset)/len(modelSubset)) < minProportion:
            minAcc -= 0.001
            accurateSubset = modelSubset[modelSubset['acc']>minAcc]
        print('minAcc:',minAcc)   
        for param in ['p1','p2','p3','p4']:
            print('\n',param,':')
            accCounts = accurateSubset[param].value_counts(sort=False)
            modCounts = modelSubset[param].value_counts(sort=False)
            newCounts = pd.DataFrame([accCounts,modCounts],index=['acc','mod'])
            newCounts = newCounts.transpose()
            newCounts.fillna(0,inplace=True)
            newCounts['Proportion'] = newCounts['acc']/newCounts['mod']
            print(newCounts)
            try:
#                plt.hist(accurateSubset[param]/modelSubset[param], bins=100)
                plt.scatter(newCounts.index, newCounts['Proportion'])
#                plt.hist(, bins=100)
                plt.show()
            except ValueError:
                print("matplotlib doesn't like strings")
            except TypeError:
                print("can't divide strings")

            
def paramScatterPlots(df, scoreToPlot='acc', subplots=False):
    assert 'OS' in df.columns, 'needs to be df with OS, p1 etc cols added'
    for model in ['NN','RF','SVM','KNN']:
        if model not in df.columns:
            continue
#        print('\nModel:',model)
        if subplots:
            if model == 'KNN':
                plt.figure(figsize=(15,5))
            else:
                plt.figure(figsize=(15,11))
        for param in ['p1','p2','p3','p4']:
            modelSubset = df[df[model]==1]
            modelSubset = modelSubset[modelSubset['OS']==0]
            modelSubset = modelSubset[modelSubset['RFE']==0]
            accurateSubset = modelSubset[modelSubset['acc']>0.72]
            labelDict = {'auc':'Area Under the ROC Curve', 'acc':'Accuracy'}
            
            # Only plot SVC degree of poly if poly is used
            if (model == 'SVM') and (param == 'p3'):
                modelSubset = modelSubset[modelSubset['p1']=='poly']
            try:
                # Choose whether subplots or normal plots
                if subplots:
                    # make KNN plots 2x1
                    if (model=='KNN'):
                        if param in ['p1','p4']:
                            continue
                        else:
                            plt.subplot(1,2,int(param[1])-1)
                    else:
                        plt.subplot(2,2,int(param[1]))
                else:
                    plt.figure(figsize=(10,6))
                
                # Plot it and put titles / axis titles
                plt.scatter(modelSubset[param],modelSubset[scoreToPlot], marker='x', s=15)
                title = f"{longNames[model]} - {paramDict[model][param]}"
                xlabel = f"{paramDict[model][param]}"
     
                # Put the label above/below the subplots so not between plots
                if (subplots and (int(param[1])>2)) and model !='KNN':
                    plt.xlabel(xlabel)
                else:
                    plt.title(title)
                
                # Log scale the x axis if it is in the list
                if any((name in title) for name in ['Alpha','Gamma','C value']):
                    plt.xscale('log')
                    plt.axis([min(modelSubset[param]), max(modelSubset[param]),
                              None, None])
                plt.ylabel(labelDict[scoreToPlot])
                plt.grid(b=True, which='major', color='black', alpha=0.2)
                if not subplots:
                    plt.show()
            except ValueError:
                print("matplotlib doesn't like strings")
        if subplots:
            plt.show()

def bestModelsBarPlot(df, score='acc', mins={}):
    assert 'OS' in df.columns, 'needs to be df with OS, p1 etc cols added'
#    plt.figure(figsize=(10,6))
    scores = {}
    xvals=[]
    yvals=[]
    print('plotting',score)
    for model in longNames.keys():     
        scores[model]={}
        modelSubset = df[df[model]==1]
        for crit, val in mins.items():
            modelSubset = modelSubset[modelSubset[crit]>val]
#        modelSubset = modelSubset[modelSubset['OS']==0]
#        modelSubset = modelSubset[modelSubset['RFE']==0]
        bestScore = modelSubset[score].max()
        scores[model][score] = bestScore
        scores[model]['runName']= df.iloc[modelSubset[score].idxmax(),0]
        xvals.append(model)
        yvals.append(bestScore)
    yvals, xvals = zip(*sorted(zip(yvals, xvals),reverse=True))
    plt.plot(xvals, yvals)
    plt.show()
    return scores

mins = {'acc':0.6, 'auc':0.6,'F1':0.25,'F0':0.25}

paramDict = {'RF': ['Scoring Criterion','Number of Estimators','Maximum Number of Features to Consider','Bootstrap used'],
             'NN': ['Solver','Number of Layers','Nodes per layer','Alpha'],
             'SVM':['Kernel Function','C value','Degree of Polynomial','Gamma value'],
             'KNN':['Algorithm','k value','p parameter','n/a'],
             }
longNames = {'RF':'Random Forest','NN':'Neural Network','SVM':'Support Vector Machine',
             'KNN':'k-Nearest Neighboours','LR':'Logistic Regression','GNB':'Gaussian Naive Bayes'}
for item in paramDict.keys():
    paramDict[item] = {('p'+str(i)):paramDict[item][i-1] for i in range(1,5)}

df = pd.read_csv(sf.addFolderPath('paramsearch3forDF7Added.csv'))
        
#paramScatterPlots(df, 'acc', subplots=True)
scores= bestModelsBarPlot(df, mins=mins)