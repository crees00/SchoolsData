# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

@author: reesc1
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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

# import statsmodels

df = pd.read_csv("dfForModelModifiedImputed.csv")

xCols = [x for x in (set(df.columns) - {"URN", "Stuck", "Unnamed: 0"})]

x = df[xCols]
y = df["Stuck"]


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
    def __init__(self, data, runParams=None):
        # data is an instance of ModelData
        self.data = data
        self.params = runParams

    def __str__(self):
        return f"{self.getLongName()} {self.getRunName()} with AUC {format(self.getAUC(),'.2f')}"

    def getData(self):
        return self.data

    def getRunName(self):
        return self.runName

    def getLongName(self):
        return self.longName

    def getFPR(self):
        return self.fpr

    def getTPR(self):
        return self.tpr

    def getAUC(self):
        return self.roc_auc

    def plotROC(self):  # fpr, tpr, runName, roc_auc, longRunName, fileName=""):
        plt.plot(
            self.getFPR(),
            self.getTPR(),
            label=self.getRunName() + " (area = %0.2f)" % self.getAUC(),
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
        self.fitLogRegModel()

    def fitLogRegModel(self):  # x_train, y_train, x_test, y_test, runName):
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


class RandomForest(Model):
    def __init__(self, dataName, data, runParams=None):
        self.runName = "RF_" + dataName
        self.longName = "Random Forest"
        Model.__init__(self, data, runParams)
        self.fitRandomForestModel()
        print(self.longName, self.runName, self.params)

    def fitRandomForestModel(self):  # x_train, y_train, x_test, y_test, runName):
        data = self.getData()
        x_train, y_train, x_test, y_test = (
            data.getxTrain(),
            data.getyTrain(),
            data.getxTest(),
            data.getyTest(),
        )
        clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0)
        clf.fit(x_train, y_train.values.ravel())
        y_pred = clf.predict(x_test)
        self.cm = confusion_matrix(y_test, y_pred)
        self.cr = classification_report(y_test, y_pred)
        self.acc = clf.score(x_test, y_test)
        self.roc_auc = roc_auc_score(y_test, clf.predict_proba(x_test)[:, 1])
        self.fpr, self.tpr, self.thresholds = roc_curve(
            y_test, clf.predict_proba(x_test)[:, 1]
        )


def oneFullRun(
    modelDataDict,
    modelDict,
    doOverSample,
    doRFE,
    modelClass,
    runParams=None,
    numColsToKeep=0,
):
    print(
        f"\nRunning",
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
    
    modelDict[mod.getRunName()] = mod
    #    fpr, tpr, runName, logit_roc_auc = model(x_train, y_train, x_test, y_test, runName)
    #    plotROC(fpr, tpr, runName, logit_roc_auc, longRunName)
    return modelDataDict, modelDict


def runsForModels(modelDataDict, modelDict, os, rfe, modelClass, num):
    if modelClass in runParams.keys():
        keys, values = zip(*runParams[modelClass].items())
        listOfRunParams = [dict(zip(keys, val)) for val in itertools.product(*values)]
        print(listOfRunParams)
        for singleRunParams in listOfRunParams:
            print('singleRunParams:',singleRunParams)
            modelDataDict, modelDict = oneFullRun(
                modelDataDict, modelDict, os, rfe, modelClass, singleRunParams, num
            )
    else:
        modelDataDict, modelDict = oneFullRun(
            modelDataDict, modelDict, os, rfe, modelClass, numColsToKeep=num
        )


def runAGroup(doOverSample, doRFE, modelClasses, numColsToKeep=0):
    modelDataDict, modelDict = {}, {}
    assert type(modelClasses) == list
    for modelClass in modelClasses:
        for os in doOverSample:
            for rfe in doRFE:
                for num in numColsToKeep:
                    modelDataDict, modelDict = runsForModels(
                        modelDataDict, modelDict, os, rfe, modelClass, num
                    )
                    if rfe == False:
                        break  # stop it doing the same thing 5x if RFE not used
    return modelDataDict, modelDict


runParams = {
    RandomForest: {"n_estimators": [10, 1000], "max_depth": [None, 10]}
}
modelDataDict, modelDict = runAGroup([False], [False], [RandomForest], [10, 20])

plt.figure(figsize=(15, 11))
for item in modelDict.values():
    item.plotROC()
    item.printOut()
plt.show()

# modelDataDict = runAGroup([True, False],[True, False],['LogReg'],[10, 20])
