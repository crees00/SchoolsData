# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

Input csv file generated by pickColsToUse.py

@author: reesc1
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    roc_auc_score,
    auc,
    classification_report,
)
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import RFE
import itertools
from random import sample
import datetime

start = datetime.datetime.now()
print(f"running genericModelClass at {start}")


# import statsmodels



class ModelData:
    def __init__(self, x, y, doOverSample, doRFE, name, numColsToKeep=0):
        self.doOverSample = doOverSample  # True/False
        self.doRFE = doRFE  # True/False
        self.name = name
        self.numColsToKeep = numColsToKeep
        self.x = x  # df with all cols
        self.y = y  # column from df
        self.xCols = x.columns

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=0.3  # random_state=0
        )

        if self.doOverSample:
            # self.x_train, self.y_train, _, _, self.y_train, self.y_test =
            self.overSample()

        if self.doRFE:
            self.recursiveFE()

    def __str__(self):
        return f"ModelData instance {self.getName()}"

    def setxTrain(self, x_train):
        self.x_train = x_train

    def setyTrain(self, y_train):
        self.y_train = y_train

    def setxTest(self, x_test):
        self.x_test = x_test

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
        os = SMOTE(random_state=0)
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
                self.runCode += ("_" + str(val))
            
            
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
            random_state=0,
            criterion=criterion,
            bootstrap=bootstrap,
        )
        clf.fit(x_train, y_train.values.ravel())
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
        self, C=1, kernel="rbf", degree=3, max_iter=-1, gamma='scale'
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
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.decision_function(x_test))
        self.fpr, self.tpr, self.thresholds = roc_curve(y_test, clf.decision_function(x_test))
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
):
    print(
        f"Running oneFullRun",
        "with oversampling" if doOverSample else "",
        f"with RFE with {numColsToKeep} cols" if doRFE else "",
    )
    dataName = ""
    #    os_data_x, os_data_y, x_train, x_test, y_train, y_test = overSample(x, y)
    if doOverSample:
        dataName += "OS" + ("_" if doRFE else "")
    if doRFE:
        dataName += "RFE" + str(numColsToKeep)
    if len(dataName) == 0:
        dataName = "original"

    if dataName not in modelDataDict:
        data = ModelData(x, y, doOverSample, doRFE, dataName, numColsToKeep)
        modelDataDict[dataName] = data
    #    print('data:',data)
    mod = modelClass(dataName, modelDataDict[dataName], runParams)
    
    #    print('mod:',mod)
    #    print('dataName:',dataName)
    #    print('modelDataDict:',modelDataDict)
#    modelDict[mod.getRunName() + (("_" + str(runNo)) if runNo > 0 else "")] = mod
    if mod.getRunCode() not in modelDict: 
        mod.fitModel(**runParams)
        modelDict[mod.getRunCode()] = mod
    #    fpr, tpr, runName, logit_roc_auc = model(x_train, y_train, x_test, y_test, runName)
    #    plotROC(fpr, tpr, runName, logit_roc_auc, longRunName)
    return modelDataDict, modelDict


def runsForModels(modelDataDict, modelDict, os, rfe, modelClass, num, numParamCombos):
    print(f"running runsForModels {(os, rfe, modelClass, num)}")
    runNo = 0
    if modelClass in runParams.keys():
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
            )
    #            print('oneFullRun done - back in runsForModels')
    else:
        modelDataDict, modelDict = oneFullRun(
            modelDataDict, modelDict, os, rfe, modelClass, numColsToKeep=num
        )
    return modelDataDict, modelDict


def runAGroup(doOverSample, doRFE, modelClasses, numColsToKeep=0, numParamCombos=10):
    print(
        f"running runAGroup with {countRuns(doOverSample, doRFE, modelClasses, numColsToKeep, numParamCombos)} runs to do"
    )
    global modelDataDict #modelDataDict = {}
    global modelDict #modelDict = {}
    assert type(modelClasses) == list
    for modelClass in modelClasses:
        for os in doOverSample:
            for rfe in doRFE:
                for num in numColsToKeep:
                    modelDataDict, modelDict = runsForModels(
                        modelDataDict,
                        modelDict,
                        os,
                        rfe,
                        modelClass,
                        num,
                        numParamCombos,
                    )
                    if rfe == False:
                        break  # stop it doing the same thing 5x if RFE not used
    return modelDataDict, modelDict


runParams = {
    RandomForest: {
        "n_estimators": [10, 50, 100, 300, 500, 800, 1000],
        "max_depth": [None, 3, 5, 8, 10],
        "criterion": ["gini", "entropy"],
        "bootstrap": [True, False],
    },
    SVM: {"C": [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1, 1.1,1.2, 1.4, 1.6, 2,2.5, 3, 3.6],
          "kernel": [
                  'linear', 
                  'poly', 
                  'rbf'
                  ],
          "degree": [2, 3, 4, 5]
          },
}
    
if __name__ == "__main__":
    df = pd.read_csv("dfForModelModifiedImputed.csv")
    xCols = [x for x in (set(df.columns) - {"URN", "Stuck", "Unnamed: 0"})]
    x = df[xCols]
    y = df["Stuck"]

    # Generate data and model instances, run the models
    modelDataDict, modelDict = runAGroup(
        [True,False], [True, False], 
        [
        SVM, 
        LogReg, 
        RandomForest
        ], [10, 20, 30], numParamCombos=20
    )
    
    # Print out ROC curve
    plt.figure(figsize=(15, 11))
    for item in modelDict.values():
        item.plotROC()
        item.printOut()
    plt.show()
    
    # Find 'best' model in dict
    maxF = 0
    for mod in modelDict.values():
        if (mod.getF1() + mod.getF0()) > maxF:
            maxF = mod.getF1() + mod.getF0()
            currMod = mod
    print(f"Best model from run is:\n{currMod}\n{currMod.getCM()}")

#import pickling
#pickling.save_dill(modelDict, 'modelDictWithDill0908')
#aReloaded = pickling.load_dill('modelDictWithDill')

# modelDataDict = runAGroup([True, False],[True, False],['LogReg'],[10, 20])
print(f"finished genericModelClass - took {datetime.datetime.now() - start}")
