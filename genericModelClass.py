# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

Input csv file generated by pickColsToUse.py

@author: reesc1
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


start = datetime.datetime.now()
print(f"running genericModelClass at {start}")


# import statsmodels


class ModelData:
    def __init__(self, x, y, doOverSample, doRFE, name, numColsToKeep=0,
                 x_train=[], x_test=[], y_train=[], y_test=[]):
        self.doOverSample = doOverSample  # True/False
        self.doRFE = doRFE  # True/False
        self.name = name
        self.numColsToKeep = numColsToKeep
        self.x = x  # df with all cols
        self.y = y  # column from df
        self.xCols = x.columns
        if len(x_train) == 0:
            print('Generating training/test split')
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=0.3  # random_state=0
            )
        else:
            print('Inputting train/test split from k-folds')
            self.x_train, self.y_train = x_train, y_train
            self.x_test, self.y_test = x_test, y_test

        if self.doOverSample:
            # self.x_train, self.y_train, _, _, self.y_train, self.y_test =
            self.overSample()

        if self.doRFE:
            self.recursiveFE()
        print("Generated", self)

    def __str__(self):
        return f"ModelData instance {self.getName()}"

    def setxTrain(self, x_train):
        self.x_train = x_train

    def setyTrain(self, y_train):
        self.y_train = y_train

    def setxTest(self, x_test):
        self.x_test = x_test
        
    def setyTest(self, y_test):
        self.y_test = y_test

    def getxTrain(self):
        return self.x_train

    def getxTest(self):
        return self.x_test

    def getyTrain(self):
        return self.y_train

    def getyTest(self):
        return self.y_test

    def getName(self):
        return self.name

    def getxCols(self):
        return self.xCols

    def getNumColsToKeep(self):
        return self.numColsToKeep

    # USE SMOTE TO OVERSAMPLE DATA I.E. MAKE MORE SYNTHETIC 'STUCK' TRAINING POINTS
    def overSample(self, toPrint=False):
        """ Inputs: x = training points in a df, y = labels col of df
        Returns dfs that are oversampled - os_data_x and os_data_y 
        plut the train/test split of the original data"""
        os = SMOTE()
        x_train, y_train = self.getxTrain(), self.getyTrain()
        #        print(f"Before oversampling, x_train has dims {x_train.shape}")
        columns = x_train.columns
        # only oversample from training data so that test data is unaffected
        os_data_x, os_data_y = os.fit_sample(x_train, y_train)
        os_data_x = pd.DataFrame(data=os_data_x, columns=columns)
        os_data_y = pd.DataFrame(data=os_data_y, columns=["y"])
        if toPrint:
            print("original x dims:", x.shape, "Original ydim:", y.shape)
            print(
                "new y value_counts (given 0.7 * 21954 = 15368 and stuck not split perfectly train 70:30 test):"
            )
            print(os_data_y["y"].value_counts())
        self.setxTrain(os_data_x)
        self.setyTrain(os_data_y)

    # Recursive feature elimination using Logistic Regression
    def recursiveFE(self, toPrint=False):
        """ Decides which features are most important to the model and returns most
        important cols.
        Inputs x & y are dfs, can either be oversampled or not.
        Returns list of cols to keep"""
        logreg = LogisticRegression(solver="lbfgs", max_iter=10000)
        rfe = RFE(logreg, self.getNumColsToKeep())
        rfe = rfe.fit(self.getxTrain(), self.getyTrain().values.ravel())
        # Choose cols that are selected by RFE
        xColsToKeep = []
        for i, col in enumerate(self.getxCols()):
            if rfe.support_[i]:
                xColsToKeep.append(col)
        if toPrint:
            print(rfe.support_)
            print(rfe.ranking_)
            print("keep:", xColsToKeep)
        self.setxTrain(self.getxTrain()[xColsToKeep])
        self.setxTest(self.getxTest()[xColsToKeep])


class Model:
    def __init__(self, data, runParams={}):
        # data is an instance of ModelData
        self.data = data
        self.params = runParams
        self.runCode = self.getRunName()
        if len(runParams) > 0:
            for val in runParams.values():
                self.runCode += "_" + str(val)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} with AUC {format(self.getAUC(),'.2f')}"

    def getData(self):
        return self.data

    def getRunName(self):
        return self.runName

    def getLongName(self):
        return self.longName

    def getRunCode(self):
        return self.runCode

    def getFPR(self):
        return self.fpr

    def getTPR(self):
        return self.tpr

    def getAUC(self):
        return self.roc_auc

    def getParams(self):
        return self.params

    def getCR(self):
        return self.cr

    def getCM(self):
        return self.cm
    
    def getAcc(self):
        return self.acc

    def getPrecision1(self):
        return self.precision1

    def getRecall1(self):
        return self.recall1

    def getPrecision0(self):
        return self.precision0

    def getRecall0(self):
        return self.recall0

    def getF1(self):
        return self.fscore1

    def getF0(self):
        return self.fscore0
    
    def getFeatureImportances(self):
        if len(self.featureImportances)>0:
            return self.featureImportances
    
    def getCLF(self):
        return self.clf
    
    def setScores(self):
        cm = self.getCM()
        self.tp = cm[1][1]
        self.tn = cm[0][0]
        self.fp = cm[0][1]
        self.fn = cm[1][0]
        self.precision1 = self.tp / (self.tp + self.fp)
        self.recall1 = self.tp / (self.tp + self.fn)
        self.precision0 = self.tn / (self.tn + self.fn)
        self.recall0 = self.tn / (self.tn + self.fp)
        self.fscore1 = (
            2
            * self.getPrecision1()
            * self.getRecall1()
            / (self.getPrecision1() + self.getRecall1())
        )
        self.fscore0 = (
            2
            * self.getPrecision0()
            * self.getRecall0()
            / (self.getPrecision0() + self.getRecall0())
        )

    def getTrainingScores(self, printOut=False):
        '''returns confusion matrix, classification report, accuracy
        of model on training set '''
        trainingPredictions = self.getCLF().predict(self.getData().getxTrain())
        trainLabels = self.getData().getyTrain()
        self.traincm = confusion_matrix(trainLabels, trainingPredictions)
        self.traincr = classification_report(trainLabels, trainingPredictions)
        self.trainacc = self.getCLF().score(self.getData().getxTrain(), trainLabels)
        if printOut:
            print(f"trainAcc = {round(self.trainacc,2)}, testAcc = {round(self.getAcc(),2)}, {self.getRunName()}")
        return self.traincm, self.traincr, self.trainacc
    
    def plotROC(self):  # fpr, tpr, runName, roc_auc, longRunName, fileName=""):
        plt.plot(
            self.getFPR(),
            self.getTPR(),
            label=self.getRunCode() + " (area = %0.2f)" % self.getAUC(),
        )
        plt.plot([0, 1], [0, 1], "r--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"Receiver Operating Characteristic for {self.getLongName()}")
        plt.legend(loc="lower right")

    def printOut(self):
        print(self)
        print(self.cm)
        print("Accuracy of classifier on test set: {:.2f}".format(self.acc))
        print(self.cr)


class LogReg(Model):
    def __init__(self, dataName, data, runParams=None):
        self.runName = "LR_" + dataName
        self.longName = "Logistic Regression"
        Model.__init__(self, data)

    #        self.fitLogRegModel()

    def fitModel(self):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        logreg = LogisticRegression(solver="lbfgs", max_iter=1000)
        logreg.fit(x_train, y_train.values.ravel())
        self.clf = logreg
        y_pred = logreg.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = logreg.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, logreg.predict_proba(x_test)[:, 1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, logreg.predict_proba(x_test)[:, 1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")


class RandomForest(Model):
    def __init__(self, dataName, data, runParams=None):
        self.runName = "RF_" + dataName
        self.longName = "Random Forest"
        Model.__init__(self, data, runParams)
        #        self.fitRandomForestModel(**self.getParams())
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self, n_estimators, max_depth, criterion="gini", bootstrap=True
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            criterion=criterion,
            bootstrap=bootstrap,
        )
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        self.featureImportances = clf.feature_importances_
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:, 1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:, 1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")


class SVM(Model):
    def __init__(self, dataName, data, runParams={}):
        self.runName = "SVM_" + dataName
        self.longName = "Support Vector Machine"
        Model.__init__(self, data, runParams)
        #        self.fitSVMModel(**self.getParams())
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} {self.getRunCode()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self, C=1, kernel="rbf", degree=3, max_iter=-1, gamma="scale"
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = SVC(C=C, kernel=kernel, degree=degree, max_iter=max_iter, gamma=gamma)
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.decision_function(x_test))
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.decision_function(x_test)
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")

class NN(Model):
    def __init__(self, dataName, data, runParams={}):
        print('starting generating a NN called',dataName,'with',runParams)
        self.runName = "NN_" + dataName
        self.longName = "Neural Network"
        Model.__init__(self, data, runParams)
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} {self.getRunCode()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self, numLayers=1, nodesPerLayer=2, solver='adam', alpha=0.0001
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        hidden_layer_sizes = tuple(list(nodesPerLayer for x in range(numLayers)))
        clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,
                            solver=solver, alpha=alpha, max_iter=1000)
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:, 1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:, 1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")

class GaussianBayes(Model):
    def __init__(self, dataName, data, runParams={}):
        self.runName = "GNB_" + dataName
        self.longName = "Gaussian Naive Bayes"
        Model.__init__(self, data, runParams)
        #        self.fitSVMModel(**self.getParams())
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} {self.getRunCode()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = GaussianNB()
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:,1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:,1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")

class KNN(Model):
    def __init__(self, dataName, data, runParams={}):
        self.runName = "KNN_" + dataName
        self.longName = "K Nearest Neighbours"
        Model.__init__(self, data, runParams)
        #        self.fitSVMModel(**self.getParams())
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} {self.getRunCode()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self, n_neighbors=2, algorithm='auto', p=2
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=algorithm, p=p)
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:,1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:,1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")

class AdaBoost(Model):
    def __init__(self, dataName, data, runParams=None):
        self.runName = "AB_" + dataName
        self.longName = "AdaBoost"
        Model.__init__(self, data, runParams)
        #        self.fitRandomForestModel(**self.getParams())
        print("Generated", self.longName, self.runName, self.params)

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} with AUC {format(self.getAUC(),'.2f')} and params {self.getParams()}"

    def fitModel(
        self, baseEstimator, nEstimators, algorithm
    ):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = AdaBoostClassifier(
        base_estimator=baseEstimator,
        n_estimators=nEstimators,
        algorithm=algorithm
        )
        clf.fit(x_train, y_train.values.ravel())
        self.clf = clf
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:, 1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:, 1]
        )
        self.setScores()
        print(f"Model fitted: {self.getRunCode()}")


def countRuns(doOverSample, doRFE, modelClasses, numColsToKeep, numParamCombos):
    runCount = len(doOverSample) * len(doRFE)
    if doRFE:
        runCount *= len(numColsToKeep)
    modelTot = 0
    for modelClass in modelClasses:
        modelCount = 1
        if modelClass in runParams.keys():
            modelCount = numParamCombos
        #            for value in runParams[modelClass].values():
        #                modelCount *= len(value)
        modelTot += modelCount
    runCount *= modelTot
    return runCount


def oneFullRun(
    modelDataDict,
    modelDict,
    doOverSample,
    doRFE,
    modelClass,
    runParams={},
    numColsToKeep=0,
    runNo=0,
    nFolds=1
):
    ''' Creates instance of ModelData and modelClass when sent the input settings
    for a single run.
    Implements k-fold cross validation
    '''
    global doneRuns
    print(
        f"Running oneFullRun",
        "with oversampling" if doOverSample else "",
        f"with RFE with {numColsToKeep} cols" if doRFE else "",
        f" -- {len(doneRuns)} runs done"
    )
    dataName = ""
    #    os_data_x, os_data_y, x_train, x_test, y_train, y_test = overSample(x, y)
    if doOverSample:
        dataName += "OS" + ("_" if doRFE else "")
    if doRFE:
        dataName += "RFE" + str(numColsToKeep)
    if len(dataName) == 0:
        dataName = "original"
    
    kf = KFold(n_splits = nFolds)
    foldIndices = []
    for trainIndices, testIndices in kf.split(x):
        foldIndices.append((trainIndices, testIndices))
    for fold in range(nFolds):
        newDataName = dataName + '_' + str(fold+1) + 'of' + str(nFolds)
        # A ModelData instance can be reused for multiple different models
        if newDataName not in modelDataDict:
            if nFolds == 1:
                data = ModelData(x, y, doOverSample, doRFE, newDataName, numColsToKeep)
            else:
                data = ModelData(x, y, doOverSample, doRFE, newDataName, numColsToKeep,
                                 x_train = x.iloc[foldIndices[fold][0],:],
                                 y_train = y[foldIndices[fold][0]],
                                 x_test = x.iloc[foldIndices[fold][1],:],
                                 y_test = y[foldIndices[fold][1]])
                
            modelDataDict[newDataName] = data
        mod = modelClass(newDataName, modelDataDict[newDataName], runParams)
    
        if (mod.getRunCode() not in modelDict) and (
        mod.getRunCode() not in doneRuns) and (
        ''.join(re.split('_[0-9]of[0-9]',mod.getRunCode())) not in doneRuns):
            mod.fitModel(**runParams)
            modelDict[mod.getRunCode()] = mod
            doneRuns.append(mod.getRunCode())
    return modelDataDict, modelDict


def runsForModels(modelDataDict, modelDict, os, rfe, modelClass, num, 
                  numParamCombos, nFolds):
    ''' Takes in a combo of input settings and a modelClass. 
    Generates random combinations of parameters for the model. 
    Sends a combination for one run to oneFullRun
    '''
    print(f"running runsForModels {(os, rfe, modelClass, num)}")
    runNo = 0
    if modelClass in runParams.keys():
        print(modelClass)
        # Generate all possible combinations of runParams
        keys, values = zip(*runParams[modelClass].items())
        listOfRunParams = [dict(zip(keys, val)) for val in itertools.product(*values)]
        if numParamCombos > len(listOfRunParams):
            sampleOfRunParamList = listOfRunParams
        else:
            sampleOfRunParamList = sample(listOfRunParams, numParamCombos)

        #        print(listOfRunParams)
        # use listOfRunParams below to try every possible combo
        for singleRunParams in sampleOfRunParamList:
            
            runNo += 1
            #            print('singleRunParams:',singleRunParams)
            modelDataDict, modelDict = oneFullRun(
                modelDataDict,
                modelDict,
                os,
                rfe,
                modelClass,
                singleRunParams,
                num,
                runNo=runNo,
                nFolds=nFolds
            )
    #            print('oneFullRun done - back in runsForModels')
    else:
        modelDataDict, modelDict = oneFullRun(
            modelDataDict, modelDict, os, rfe, modelClass, numColsToKeep=num,
            nFolds=nFolds
        )
    return modelDataDict, modelDict


def runAGroup(doOverSample, doRFE, modelClasses, numColsToKeep=0, 
              numParamCombos=10, nFolds=1):
    ''' Takes in all the options as inputs and runs through each combination of
    input data options, sending them to runsForModels
    '''
    print(
        f"running runAGroup with {countRuns(doOverSample, doRFE, modelClasses, numColsToKeep, numParamCombos)} runs to do"
    )
    global modelDataDict  # modelDataDict = {}
    global modelDict  # modelDict = {}
    global doneRuns
    try:
        modelDataDict
    except NameError:
        print("new modelDataDict")
        modelDataDict = {}
    try:
        modelDict
    except NameError:
        print("new modelDict")
        modelDict = {}
    assert type(modelClasses) == list
    for modelClass in modelClasses:
        for os in doOverSample:
            for rfe in doRFE:
                for num in numColsToKeep:
                    print(f'\nlen(modelDict): {len(modelDict)}\n')
                    if len(modelDict)>400:
                        #try:
                        postProcess(modelDataDict, modelDict,pickleIt=False)
                        modelDict={}
                    modelDataDict, modelDict = runsForModels(
                        modelDataDict,
                        modelDict,
                        os,
                        rfe,
                        modelClass,
                        num,
                        numParamCombos,
                        nFolds
                    )
                    if rfe == False:
                        break  # stop it doing the same thing 5x if RFE not used
        
        try:
            content = f"finished {modelClass} runs - took {datetime.datetime.now() - start} and now there are {len(doneRuns)} models"
            emailing.sendEmail(subject="Some runs done", content=content)
        except:
            print("\nEmail sending  for run type failed, carrying on..\n")

    return modelDataDict, modelDict

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
        outDF.to_csv(sf.addFolderPath( write))
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
        for score in (set(runResultsDict.keys()) - 
                      {'cr','longName','params','runCode','runName','tpr','fpr','cm'}):
            modelAvgDict[runName][score] = np.mean(runResultsDict[score])
            modelAvgDict[runName]['acc variance'] = np.var(runResultsDict['acc'])
    
    if len(write)>0:
        outDF = pd.DataFrame(modelAvgDict)
        outDF.to_csv(sf.addFolderPath(write))
        print(write,'file written')
#
    return modelAvgDict, modelScoresDict


def postProcess(modelDataDict, modelDict, pickleIt=False, emailIt=True, ROC=False):
    now = datetime.datetime.now()
    modelAvgDict, modelScoresDict = makeAvgResults(modelDict,  'AVG'  + str(now.day)
        + "_"
        + str(now.month)
        + "_"
        + str(now.hour)
        + str(now.minute)
        + fileName
)
            
    # Find 'best' model in dict
    maxAcc= 0
    currModAcc=''
    for runName in modelAvgDict.keys():
        if modelAvgDict[runName]['acc'] > maxAcc:
            maxAcc = modelAvgDict[runName]['acc']
            currModAcc = runName
#    print(f"Best model for F from run is:\n{currModF}\n{currModF.getCM()}")
    print(f"Best model for accuracy from run is:\n{currModAcc}")
    print(f"Accuracy: {maxAcc}")
    
    if pickleIt:    
        import pickling
        pickling.save_dill(
            modelDict,
            "modelDict"
            + str(now.day)
            + "_"
            + str(now.month)
            + "_"
            + str(now.hour)
            + str(now.minute),
        )
    # Save results in .csv file
    
    exportResultsDF(modelDict, "modelDict"
        + str(now.day)
        + "_"
        + str(now.month)
        + "_"
        + str(now.hour)
        + str(now.minute)
        + fileName
    )
    if ROC:
        # Print out ROC curve
        plt.figure(figsize=(15, 11))
        for item in modelDict.values():
            item.plotROC()
    #        item.printOut()
        plt.show()
    if emailIt:
        try:
            content = f"finished genericModelClass - took {datetime.datetime.now() - start} and ran {len(modelDict)-modelsAtStart} models\n{currModAcc} {maxAcc}"
            emailing.sendEmail(subject=f"{maxAcc}, {currModAcc}", content=content)
        except:
            print("\nEmail sending failed, carrying on..\n")
    return modelAvgDict, modelScoresDict

def findFIsFromDict(modelDict, toPrint=True):
    '''Takes in a modelDict with the CV runs from a single run
    Prints features in reverse order of importance
    Returns FIarray - a df with a col for each of the CV runs + an average col
    '''
    FIarray = 'justastring'
    for model in modelDict.values():
        FIarray = featureImportances(model, FIarray)
    indices = np.argsort(model.getFeatureImportances())[::-1]
    FIarraySorted = FIarray.sort_values('Avg', ascending=False)
    if toPrint:
        print("Feature ranking:")
        print(FIarraySorted['Avg'])
#        for f in range(model.getData().getxTrain().shape[1]):
#            print("%d. feature %d (%f)" % (f + 1, indices[f], model.getFeatureImportances()[indices[f]]))
#            print(model.getData().getxCols()[indices[f]])
    return FIarray

def featureImportances(model, FIarray='nothing'):
    newCol = pd.DataFrame(model.getFeatureImportances(), index=model.getData().getxCols(),
                          columns = [model.getData().name[-4:]])
    # Start a new array if nothing fed in
    if type(FIarray)==str:
        FIarray=newCol
    else:
        # else add on the col to the existing array
        FIarray = pd.concat([FIarray, newCol], axis=1)  
        # if final run e.g. 5 of 5
        if model.getData().name[-4] == model.getData().name[-1]:
            FIarray['Avg'] = FIarray.apply(np.mean, axis=1)
    return FIarray

runParams = {
    RandomForest: {
        "n_estimators":list(range(2,300,2))+ list(range(12,2000,20)),#[10, 30, 50, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200,210, 220,230, 240, 250,260,270,280,500],
        "max_depth": list(range(1,30)) + list(range(4,19)),#[11,12,13,14,15,16],#[4,5,6,7,8,9,10,11,12,13,14,15,16],
        "criterion": ['entropy','gini'],#["gini", "entropy"],
        "bootstrap": [False, True]#[True, False],
    },
    SVM: {
        "C": list(np.logspace(-3,1)) + list(np.linspace(0.4,12,100)),#[1,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.8,3,3.2,3.4,3.6,4,5,6,8,10,15,20,30,50],
        "kernel": ["rbf",'poly'],
        "degree":[1,2,3],
        "gamma": list(np.linspace(0.001,0.05,200)) + list(np.logspace(-3,0)),#[0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5,0.6,0.7,0.8]
    },
    NN: {
        'numLayers' : [1,2,3,4,5,6,7],
        'nodesPerLayer' : list(range(1,20)),
        'solver' : ['adam','lbfgs','sgd'], 
        'alpha' : list(np.logspace(-8,-1))+list(np.linspace(0.00001,0.3,num=30))
    },
    KNN: {
        'n_neighbors':range(1,50),#[1,2,3,4,6,8,12,15,20,25],
        'algorithm':['brute','auto'],
        'p':[1,2,3]
    } ,
    AdaBoost: {
        'baseEstimator':[RandomForestClassifier(max_depth=11, n_estimators=200), 
#                         SVC(C=5)
                         LogisticRegression(),
                         GaussianNB()
                         ], 
        'nEstimators':[10,100,1000,10000],
        'algorithm':['SAMME']#'SAMME.R',
            }
}

colDict = {'SVM':{'cols':CS.SVMcols2, 'model':SVM},
           'NN' :{'cols':CS.NNcols2, 'model':NN},
           'KNN':{'cols':CS.KNNcols2, 'model':KNN},
           'RF' :{'cols':CS.RFcols2, 'model':RandomForest},
           'LR':{'cols':CS.LRcols, 'model':LogReg},
           'GNB':{'cols':CS.GNBcols, 'model':GaussianBayes},
#           'AB':{'cols':CS.RFcols2, 'model':AdaBoost}
           }

if __name__ == "__main__":
    import emailing
    import pickling
#    doneRuns=[]
    files = ['stuckForDF7.csv']*1000#'bbbbVgsbbbsdf7.csv']#*1000
    for fileName in files:#['bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv','bbbbVgsbbbs6.csv']:#,'bbbbVgsbbbsAllCols.csv']:#,'bbbVgsbbsLessCols.csv','bbbVgbbLessCols.csv', 'bbbbVgbbbLessCols.csv']:
#        for cols in [CS.KNNcols]:#[SFS1Cols,SFS2Cols,chosenCols1, lessCols, cols]:   
        for modelType in colDict.keys():#['GNB','LR','KNN','SVM','NN','RF']:
            pickling.save_dill(doneRuns, f"doneRuns_{len(doneRuns)}")
#            modelDict={}
            modelDataDict={}
            df = pd.read_csv(sf.addFolderPath( fileName))
            cols = colDict[modelType]['cols']
#            cols = list(df.columns)
#            xCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]
#            cols.append('PerformancePctRank')
            xCols = [x for x in (set(cols) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1','PTRWM_EXP__18','GOR_Not Applicable'})]
            x = df[xCols]
            print(x.columns)
            y = df["Class"]
            try:
                modelsAtStart = len(modelDict)
            except NameError:
                modelsAtStart = 0
            # Generate data and model instances, run the models
            modelDataDict, modelDict = runAGroup(
                [
                        True, 
#                        False,
                        False
                 ],
                [
                        True,
#                        False,
                        False
                        ],
                [
                        colDict[modelType]['model']
#                        LogReg, 
#                        SVM, 
#                        RandomForest,
#                        NN,
#                        GaussianBayes,
#                        KNN
                        ],
                [5,10,20],
                numParamCombos=5,
                nFolds = 5
            )
            modelAvgDict, modelScoresDict = postProcess(modelDataDict, modelDict)
#            findFIsFromDict(modelDict)
            print(f"finished genericModelClass - took {datetime.datetime.now() - start}")


#    pass
# import pickling
# pickling.save_dill(modelDict, 'modelDictWithDill0908')
# aReloaded = pickling.load_dill('modelDictWithDill')

# modelDataDict = runAGroup([True, False],[True, False],['LogReg'],[10, 20])
