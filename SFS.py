# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:10:58 2019

Sequential Forward Selection of features

@author: Chris
"""

import genericModelClass as gmc
import pandas as pd
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC

csv ='bbbbVgsbbbsWithPTRWM.csv'#:#,'bbbbVgsbbbsAllCols.csv']:#,'bbbVgsbbsLessCols.csv','bbbVgbbLessCols.csv', 'bbbbVgbbbLessCols.csv']:
df = pd.read_csv(csv)
xCols = [x for x in (set(df.columns) - {"URN", "Stuck","Class", "Unnamed: 0",'Unnamed: 0.1'})]
x = df[xCols]
y = df["Class"]

runDict = {'SVM_RFE10_1.6_rbf_4_0.08':{'clf':SVC(C=1.6, gamma=0.08)},
           'SVM_RFE10_2.5_rbf_5_0.05':{'clf':SVC(C=2.5, gamma=0.05)},
           'SVM_RFE10_2_rbf_3_0.09' :{'clf':SVC(C=2, gamma=0.09)},
           'SVM_RFE10_1.4_rbf_5_0.06':{'clf': SVC(C=1.4, gamma=0.06)},
           'RF_OS_4of5_10_5_entropy_True':{'clf':RandomForestClassifier(n_estimators=10, max_depth=5, criterion='entropy', bootstrap=True)}

        }

for runName, subDict in runDict.items():
    for forward in [True,False]:
        if forward:
            k_features = (3,35)
        else:
            k_features = (35,3)
        featureSelector = SequentialFeatureSelector(
            subDict['clf'],
            k_features=k_features,
            forward=forward,
            verbose=2,
            scoring="accuracy",
            cv=5,
            n_jobs=-1
        )
        if forward:
            subDict['Ffeatures'] = featureSelector.fit(x,y)
            subDict['FfilteredFeatures'] = x.columns[list(subDict['Ffeatures'].k_feature_idx_)]
        else:
            subDict['Bfeatures'] = featureSelector.fit(x,y)
            subDict['BfilteredFeatures'] = x.columns[list(subDict['Bfeatures'].k_feature_idx_)]
            
#print(filteredFeatures)