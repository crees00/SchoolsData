# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 10:04:33 2019

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

if __name__ == "__main__":
    import pickling
    from genericModelClass import colDict
#    doneRuns=[]
    fileName='bbbbVgsbbbsdf7.csv'
    for modelType in ['GNB','LR','KNN','SVM','NN','RF']:
#            modelDict={}
        df = pd.read_csv(sf.addFolderPath( fileName))
        cols = colDict[modelType]['cols']
        xCols = [x for x in (set(cols) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1','PTRWM_EXP__18','GOR_Not Applicable'})]
        x = df[xCols]
        y = df["Class"]
        try:
            modelsAtStart = len(modelDict)
        except NameError:
            modelsAtStart = 0
        clf = AdaBoostClassifier(n_estimators=100)
        xtrain, ytrain, xtest, ytest = train_test_split()
        clf.fit(x,y)
        print(clf.score(x,y))