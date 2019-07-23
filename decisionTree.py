# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019

@author: reesc1
"""

from sklearn import tree
import pandas as pd
import graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree.export import export_text

df = pd.read_csv('dfForModelModified.csv')

xCols = [x for x in (set(df.columns) - {'URN','Stuck','Unnamed: 0'})]


noBlanks = df[df.apply(lambda x: x.count(),axis=1) > 44]

x = noBlanks[xCols]
y = noBlanks['Stuck']

clf = tree.DecisionTreeClassifier( max_depth = 5)
clf = clf.fit(x,y)

tree.plot_tree(clf)

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
r = export_text(clf, feature_names=xCols)