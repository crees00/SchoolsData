# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

@author: reesc1
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import pandas as pd


df = pd.read_csv('dfForModelModified.csv')

xCols = [x for x in (set(df.columns) - {'URN','Stuck','Unnamed: 0'})]


noBlanks = df[df.apply(lambda x: x.count(),axis=1) > 44]
numberToTry = 1000

x = noBlanks[xCols]
y = noBlanks['Stuck']

clf = LogisticRegression(solver = 'lbfgs').fit(x,y)

pred = clf.predict(x)
prob = clf.predict_proba(x.iloc[:numberToTry,:])

for example in range(numberToTry):
    print(y.iloc[example], pred[example])
    
print(confusion_matrix(y, pred))