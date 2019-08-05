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
from sklearn.metrics import confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt

df = pd.read_csv("dfForModelModifiedImputed.csv")

xCols = [x for x in (set(df.columns) - {"URN", "Stuck", "Unnamed: 0"})]


#noBlanks = df[df.apply(lambda x: x.count(), axis=1) > 44]

x = df[xCols]
y = df["Stuck"]

clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(x, y)

fig, ax = plt.subplots()
fig.set_figheight(12)
fig.set_figwidth(15)
tree.plot_tree(clf, ax=ax)

#dot_data = tree.export_graphviz(clf, out_file=None)
#graph = graphviz.Source(dot_data)
r = export_text(clf, feature_names=xCols)
print(r)

print(confusion_matrix(y, clf.predict(x)))


# Compute ROC curve and ROC area for each class
fpr = []
tpr = []
roc_auc = dict()
plt.figure()

# ROC curve for different max depths for tree
for i in range(2,10):
    clf = tree.DecisionTreeClassifier(max_depth=i)
    clf = clf.fit(x, y)
    cm = confusion_matrix(y, clf.predict(x))
#    fpr[i], tpr[i], _ = roc_curve(y, clf.predict(x))
#    roc_auc[i] = auc(fpr[i], tpr[i])
    [[tn, fp],[fn, tp]] = cm
    fpr.append(fp/ (tn+fp))
    tpr.append(tp/(tp+fn))
    recall = tp/(tp + fn)
    precision = tp/(tp + fp)
    fMeasure = 2*recall*precision/(recall+precision)
    print(i, '\n',confusion_matrix(y, clf.predict(x)))
    print('F-measure:',fMeasure)
    
lw = 2
plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC')#,label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()