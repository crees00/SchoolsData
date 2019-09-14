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

def bestModelsBarPlot(df, score='acc', mins={}, show=True, xvals=None, sameRuns=True, bestRuns=None, ymax=None):
    '''fed by makeSubplots or can be used on its own. 
    Plots a single bar plot
    sorts by value unless an ordering (xvals) is passed in
    If sameRuns is used, then the individual runs in the first plot are 
    saved in bestRuns and looked up and plotted in the rest of the charts'''
    assert 'OS' in df.columns, 'needs to be df with OS, p1 etc cols added'
    from math import ceil
#    plt.figure(figsize=(10,6))
    scores = {}
    newxvals=[]
    yvals=[]
    print('plotting',score)
    for model in longRunNames.keys():     
        scores[model]={}
        modelSubset = df[df[model]==1]
        for crit, val in mins.items():
            modelSubset = modelSubset[modelSubset[crit]>val]
            if len(modelSubset)==0:
                print(model, crit, val,'No values left in df after setting minimums')
                break
        if len(modelSubset)==0:
            continue
#        modelSubset = modelSubset[modelSubset['OS']==0]
#        modelSubset = modelSubset[modelSubset['RFE']==0]
        bestScore = modelSubset[score].max()
        scores[model][score] = bestScore
        scores[model]['runName']= df.iloc[modelSubset[score].idxmax(),0]
        newxvals.append(model)
        yvals.append(bestScore)
#    print(xvals)
    # if xvals is true then it is not the first run and so use existing xvals
    if xvals:
        yvals = [scores[model][score] for model in xvals]
        if sameRuns:
            yvals = [float(df[df.iloc[:,0]==runName][score].values) for runName in bestRuns]
    # if xvals=None then it is the first run so use newxvals generated in loop
    else:
        yvals, xvals = zip(*sorted(zip(yvals, newxvals),reverse=True))
        bestRuns = [scores[model]['runName'] for model in xvals]
#    print(yvals)
    plt.bar(xvals, yvals)
    if ymax:
        plt.yticks([x/10 for x in range(10*ymax+1)])
        
        plt.ylim([0,ymax])
    else:
        plt.ylim([0,ceil((max(yvals))*10)/10])
    plt.grid(axis='y',which='both', visible=True)
#    print(scores)
    print(bestRuns)
    if show:
        plt.show()
    return xvals, bestRuns

def makeSubplots(df, measureList, mins, figsize=(10,6), sameRuns=True, ymax=None,
                 chosenMeasure=None):
    ''' Takes a list of measures and makes subplots, each one being a bestModelsBarPlot
    makes x order the same in all plots - first one sorted then the other plots follow'''
    plt.figure(figsize=figsize)
    xvals=None
    bestRuns=None
    if chosenMeasure:
        xvals, bestRuns = bestModelsBarPlot(df,chosenMeasure, show=False, xvals=xvals, 
                                            sameRuns=sameRuns, bestRuns=bestRuns,
                                            mins=mins, ymax=ymax)
    for i,measure in enumerate(measureList):
        i+=1
        plt.subplot(1,len(measureList),i)
        plt.title(longMeasureNames[measure])
        xvals, bestRuns = bestModelsBarPlot(df,measure, show=False, xvals=xvals, 
                                            sameRuns=sameRuns, bestRuns=bestRuns,
                                            mins=mins, ymax=ymax)
    print(xvals)
    
    
def RFEBarPlot(df, score='acc', mins={}, RFE=False, OS=False, subPlots=False, barwidth=1):
    '''
    Plots a single bar plot
'''
    assert 'OS' in df.columns, 'needs to be df with OS, p1 etc cols added'
    assert (OS or RFE), 'select OS or RFE'
    from math import ceil
#    plt.figure(figsize=(10,6))
    print('plotting',score)
    if subPlots:
        plt.figure(figsize=(15,7))
        plt.suptitle(f"{longMeasureNames[score]} of best run when {'Oversampling is used' if OS else ('selecting different numbers of features using RFE' if RFE else '')}")
    for i,model in enumerate(longRunNames.keys()):     
        modelSubset = df[df[model]==1]
        for crit, val in mins.items():
            modelSubset = modelSubset[modelSubset[crit]>val]
        if RFE:
            xvals,yvals = [],[]
            for RFEval in set(df['RFE']):
                RFEsubset = modelSubset[modelSubset['RFE']==RFEval]
                if RFEval==0:
                    RFEval=30
                xvals.append(RFEval)
                yvals.append(RFEsubset[score].max())
            # put no RFE (RFE=0) last
#            xvals.append(xvals.pop(0))
#            yvals.append(yvals.pop(0))
        if OS:
            xvals,yvals=[],[]
            for OSval in [0,1]:
                OSsubset = modelSubset[modelSubset['OS']==OSval]
                xvals.append(OSval)
                yvals.append(OSsubset[score].max())
        if subPlots:
             plt.subplot(1,len(longRunNames),i+1)
        plt.bar(xvals, yvals, width=barwidth)
        plt.grid(axis='y')
        if RFE:
            plt.xlim([min(xvals)-2, max(xvals)+2])
        plt.xticks(ticks=xvals,labels=[longAxisNames[f"{'OS' if OS else 'RFE'}"][x] for x in xvals])
        if subPlots:
            plt.title(f"{longRunNames[model]}")
            plt.ylim([0,ceil((max(df[score]))*10)/10])
        else:
            plt.title(f"{'Using oversampling' if OS else ('Applying different levels of RFE' if RFE else '')} for {longRunNames[model]}")
            plt.ylabel(longMeasureNames[score])
            plt.ylim([0,ceil((max(yvals))*10)/10])
        if not subPlots:
            plt.show()    

def findParamsOfBestRuns(df, numBest=5, measure='auc', mins={}):
    ''' make a dictionary (scores) with the parameters of the best 5 runs
    according to a certain parameter '''
    scores={}
    df = df.sort_values(measure, ascending=False)
    for model in longRunNames.keys():     
        modDict={name:[] for name in ['RFE', 'OS', 'p1', 'p2', 'p3', 'p4']}
        modelSubset = df[df[model]==1]
        modelSubset = modelSubset.iloc[:5,:]
        for crit, val in mins.items():
            modelSubset = modelSubset[modelSubset[crit]>val]
        
        for item in modDict.keys():
            modDict[item] = list(set(modelSubset[item].dropna()))
        scores[model] = modDict
    return scores
    
def plotPrecisionVsRecall(df, mins):
    for crit, val in mins.items():
        df = df[df[crit]>val]
    if len(df)==0:
        raise 'no points greater than the minimums'
        

# plt.style.available
mins = {'acc':0.6,
        'auc':0.6,
        'F1':0.25,
        'F0':0.25,
        'recall1':0.1,
        'recall0':0.1,
        'precision1':0.1
        }

paramDict = {'RF': ['Scoring Criterion','Number of Estimators','Maximum Number of Features to Consider','Bootstrap used'],
             'NN': ['Solver','Number of Layers','Nodes per layer','Alpha'],
             'SVM':['Kernel Function','C value','Degree of Polynomial','Gamma value'],
             'KNN':['Algorithm','k value','p parameter','n/a'],
             }
longRunNames = {'RF':'Random Forest','NN':'Neural Network','SVM':'Support Vector Machine',
             'KNN':'k-Nearest Neighboours','LR':'Logistic Regression','GNB':'Gaussian Naive Bayes'}
longMeasureNames = {'acc':'Accuracy','auc':'Area Under the ROC curve',
                    'recall1':'Recall of Class=1','recall0':'Recall of Class=0',
                    'precision1':'Precision for Class=1','precision0':'Precision of Class=0'}
longAxisNames={'OS':{0:'No OS', 1:'OS'},
               'RFE':{30:'No\nRFE', 5:'5',10:'10',15:'15',
                      20:'20',25:'25'}}
for item in paramDict.keys():
    paramDict[item] = {('p'+str(i)):paramDict[item][i-1] for i in range(1,5)}

df = pd.read_csv(sf.addFolderPath('paramsearch3forDF7Added.csv'))
#df = pd.read_csv(sf.addFolderPath('paramsearch1OldStuckAdded.csv'))
        
measureList=['auc','acc','recall1','recall0','precision1','precision0']
#paramScatterPlots(df, 'acc', subplots=True)
#scores= bestModelsBarPlot(df, mins=mins)
makeSubplots(df, measureList, mins=mins, figsize=(15,7), ymax=1, chosenMeasure='precision1')
#
#for score in measureList:
#    RFEBarPlot(df, score=score,OS=True, subPlots=True, mins=mins, barwidth=0.3)

#scores = findParamsOfBestRuns(df, mins=mins)