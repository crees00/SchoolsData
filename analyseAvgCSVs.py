# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:20:46 2019

@author: Chris
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from os import listdir
import setFolder as sf

def makeCSVlistFromFolderName(folderName, basePath = sf.folderPath):
    '''Make a list of all the filenames in a folder'''
#    basePath = ''
#    fullPath = basePath + folderName
#    print(fullPath)
    listofcsvs = listdir(sf.addFolderPath(folderName) )
    
#    print(listofcsvs)
    listofcsvs = [sf.addFolderPath(x, folderName=folderName) for x in listofcsvs]
#    print(listofcsvs)
    return listofcsvs

def combineIntermediateResultsCSVs(listOfCSVFilenames, outFile=''):
    ''' Runs take too much memory and crash computer so at intervals it dumps
    the results to csv and wipes the memory clean. This function is just to 
    stitch the csv files together so the results are all in one place
    '''
    global dupLists
#    global droppedCols
    dupLists = {}
    allDups = []
    bigDF = pd.read_csv(listOfCSVFilenames[0])
    bigDF.set_index(keys='Unnamed: 0')
    droppedCols = {'test'}
    droppedTingsTest = []
    for fileName in listOfCSVFilenames[1:]:
        nextDFtoJoin = pd.read_csv(fileName)
        colsToDrop = set(bigDF.columns) & set(nextDFtoJoin.columns)
        
        colsToDrop = colsToDrop | {'Unnamed: 0'}
        droppedTingsTest.append(colsToDrop)
        droppedCols = droppedCols | colsToDrop
#        print(colsToDrop)
        for col in colsToDrop:
            if col in nextDFtoJoin.columns:
                nextDFtoJoin.drop(col, axis=1, inplace=True)
        bigDF = bigDF.join(nextDFtoJoin)#, rsuffix='_'+fileName[:-4]+'_DUP')
        
        for col in bigDF.columns:
            if col[-4:]=='_DUP':
                if col not in allDups:
                    allDups.append(col)
                    try:
                        dupLists[fileName].append(col)
                    except KeyError:
                        dupLists[fileName] = [col]
    if outFile !='':
        bigDF.to_csv(sf.addFolderPath(outFile), index=False)
    return bigDF

def processCSV(csv, write=False, addCols=True):
    ''' Takes in avg results csv
    Reads run name and extracts run info, putting into cols to use later 
    for plotting etc.
    Adds one hot cols for RFE & OS
    Adds p1/2/3/4 cols with the param values for that run
    '''
    if type(csv)==str:
        df = pd.read_csv(sf.addFolderPath(csv))
    else:
        df = csv
    df.set_index('Unnamed: 0', inplace=True)
    df = df.sort_values(by='acc', axis=1, ascending=False)
    df = df.transpose()
    print(f'Analysing {csv}:')
    # Make subset of df that has the minimum scores in the dict
    dfWithMins = df.copy()
    minScores = {'acc':0.5, 'recall1':0.3, 'F0':0.1, 'F1':0.1, 'precision0':0.1}
    for measure, score in minScores.items():
        dfWithMins = df[df[measure]>score]

        best = {}
    for col in ['F0', 'F1', 'acc', 'auc', 'precision0', 'precision1',
       'recall0', 'recall1']:
        print(f"Best {col}:")
        runName = dfWithMins.loc[:,col].idxmax()
        best[col] = (dfWithMins.loc[:,col].max(),runName, dfWithMins.loc[runName, :])
        print(best[col][0],'for',best[col][1])
#        print(best[col][2])
        

    
    df.columns.rename('Run', inplace=True)
    
#    df=df.head(100)
    if addCols:
    #    df['RunName'] = df.index
        df['Model'] = None
        df['RFE'] = None
        df['OS'] = None
        df['p1'] , df['p2'], df['p3'], df['p4'] = None, None, None, None
        for runName in df.index:
            # Identify model type in 'Model' col
            nameDict = {'SV':'SVM','NN':'NN','RF':'RF','GN':'GNB','LR':'LR','KN':'KNN'}
            df.loc[runName,'Model'] = nameDict[runName[:2]]
            end=3
            if runName[:2] in ['GN','SV','KN']:
                end=4
    
    #        end = len(df.loc[runName,'Model'])+1
            # Put no. of RFE vals in RFE col - 0 if RFE not used
            if len(re.findall('RFE',runName)) >0:
                RFE= runName[runName.find('RFE')+3:runName.find('RFE')+5]
                try:
                    RFE = int(RFE)
                    end+=6
                except ValueError:
                    RFE = int(RFE[0])
                    end+=5
            else:
                RFE=0
            df.loc[runName, 'RFE'] = RFE
            
            # Put 1 in 'OS' col if oversampled
            if len(re.findall('OS',runName)) >0:
                df.loc[runName,'OS']= 1
                end+=3
            else:
                df.loc[runName,'OS']=0
            # Fix for 'original'
            if end <5:
                end += 9
                
            # Sort out params
            if runName[:2] in ['SV', 'NN', 'RF','KN']:
                bits = []
                string = ''
                for char in runName[end:len(runName)]:
                    if char=='_':
                        if string == 'None':
                            string=20
                        try:
                            string = float(string)
                            bits.append(string)
                        except ValueError:
                            bits.insert(0,string)
                        string=''
                    else:
                        string += char
                if string =='False':
                    string=0
                elif string=='True':
                    string=1
                bits.append(float(string))
                for i, param in enumerate(['p1','p2','p3','p4']):
                    if (runName[:2] == 'KN') and i==3:
                        df.loc[runName,param]=0
                    else:
                        df.loc[runName,param]=bits[i]
        # Make model type one hot
        df = pd.get_dummies(df,columns=['Model'], prefix='', prefix_sep='')
        
        if write:
            df.to_csv(sf.addFolderPath(csv[:-4] + 'Added.csv'))
    
    return df

def paramHistograms(df, minAcc=0.60, minProportion=-1):
    ''' If a minProportion is set to e.g. 0.1 then accurateSubset for that
    model will be the most accurate 10% of runs for that model.
    If no minProportion set, uses minAcc set or minAcc default
    '''
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
    for model in ['NN','RF','SVM','KNN']:
        if model not in df.columns:
            continue
#        print('\nModel:',model)
        if subplots:
            plt.figure(figsize=(15,9))
        for param in ['p1','p2','p3','p4']:
            modelSubset = df[df[model]==1]
            modelSubset = modelSubset[modelSubset['OS']==0]
            modelSubset = modelSubset[modelSubset['RFE']==0]
            accurateSubset = modelSubset[modelSubset['acc']>0.72]
            labelDict = {'auc':'Area Under the ROC Curve', 'acc':'Accuracy'}
            if (model == 'SVM') and (param == 'p3'):
                modelSubset = modelSubset[modelSubset['p1']=='poly']
            try:
                if subplots:
                    plt.subplot(2,2,int(param[1]))
                else:
                    plt.figure(figsize=(10,6))
                plt.scatter(modelSubset[param],modelSubset[scoreToPlot], marker='x', s=15)
                title = f"{longNames[model]} - {paramDict[model][param]}"
                xlabel = f"{paramDict[model][param]}"
                if subplots and (int(param[1])>2):
                    plt.xlabel(xlabel)
                else:
                    plt.title(title)
                plt.ylabel(labelDict[scoreToPlot])
                plt.grid(b=True, which='major', color='black', alpha=0.2)
                if not subplots:
                    plt.show()
            except ValueError:
                print("matplotlib doesn't like strings")
        if subplots:
            plt.show()
#RFparams = ['Scoring Criterion','Number of Estimators','Maximum Depth','Bootstrap used']
#NNparams = ['Solver','Number of Layers','Nodes per layer','Alpha']
paramDict = {'RF': ['Scoring Criterion','Number of Estimators','Maximum Depth','Bootstrap used'],
             'NN': ['Solver','Number of Layers','Nodes per layer','Alpha'],
             'SVM':['Kernel Function','C value','Degree of Polynomial','Gamma value'],
             'KNN':['Algorithm','k value','p parameter','n/a'],
             }
longNames = {'RF':'Random Forest','NN':'Neural Network','SVM':'Support Vector Machine','KNN':'k-Nearest Neighboours'}
for item in paramDict.keys():
    paramDict[item] = {('p'+str(i)):paramDict[item][i-1] for i in range(1,5)}
#RFdict = {('p'+str(i)):RFparams[i-1] for i in range(1,5)}
#listofcsvs = makeCSVlistFromFolderName('KNNinitialparamsearch')
#outFile = 'fullBashsep4ChosenCols1.csv' #this one for intermediate big paramsearch 
outFile='KNNinitialSearch.csv'
##outFile = 'AVG26_8_119bbbbVgsbbbsLessColsAdded.csv'
##df = pd.read_csv(sf.addFolderPath( 'AVG26_8_119bbbbVgsbbbsLessColsAdded.csv'))
#df = combineIntermediateResultsCSVs(listofcsvs, outFile)
df = processCSV(outFile, write=False, addCols=True)
##df1 = processCSV('AVG26_8_119bbbbVgsbbbsLessCols.csv', write=False, addCols=True)
## ^ This one used for choosing parameters..mysteriously high results
#df2 = processCSV('AVG26_8_757bbbbVgsbbbsAllCols.csv')
#paramHistograms(df, minProportion=0.01)
#
        
paramScatterPlots(df, 'acc', subplots=True)
#paramScatterPlots(df1, 'acc', subplots=True)