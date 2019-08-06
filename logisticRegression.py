# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:45 2019
https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
@author: reesc1
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
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

# import statsmodels

df = pd.read_csv("dfForModelModifiedImputed.csv")

xCols = [x for x in (set(df.columns) - {"URN", "Stuck", "Unnamed: 0"})]

x = df[xCols]
y = df["Stuck"]

# USE SMOTE TO OVERSAMPLE DATA I.E. MAKE MORE SYNTHETIC 'STUCK' TRAINING POINTS
def overSample(x, y, toPrint=False):
    """ Inputs: x = training points in a df, y = labels col of df
    Returns dfs that are oversampled - os_data_x and os_data_y 
    plut the train/test split of the original data"""
    os = SMOTE(random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, #random_state=0
    )
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
    return os_data_x, os_data_y, x_train, x_test, y_train, y_test


# Recursive feature elimination
def recursiveFE(numColsToKeep, x, y, toPrint=False):
    """ Decides which features are most important to the model and returns most
    important cols.
    Inputs x & y are dfs, can either be oversampled or not.
    Returns list of cols to keep"""
    logreg = LogisticRegression(solver="lbfgs", max_iter=10000)
    rfe = RFE(logreg, numColsToKeep)
    rfe = rfe.fit(x, y.values.ravel())
    # Choose cols that are selected by RFE
    xColsToKeep = []
    for i, col in enumerate(xCols):
        if rfe.support_[i]:
            xColsToKeep.append(col)
    if toPrint:
        print(rfe.support_)
        print(rfe.ranking_)
        print("keep:", xColsToKeep)
    return xColsToKeep


# Implementing the model - doesn't work as can't import statsmodels without error
# logit_model = statsmodels.api.Logit(y,x)
# result = logit_model.fit()
# print(result.summary2())

# Model fitting
def fitLogRegModel(os_data_x, os_data_y, x_test, y_test, xColsToKeep, runName):
    print(x_test[xColsToKeep].shape)
    logreg = LogisticRegression(solver="lbfgs", max_iter=1000)
    logreg.fit(os_data_x[xColsToKeep], os_data_y.values.ravel())
    y_pred = logreg.predict(x_test[xColsToKeep])
    print(
        "Accuracy of logistic regression classifier on test set: {:.2f}".format(
            logreg.score(x_test[xColsToKeep], y_test)
        )
    )
    #    confusion_matrix = confusion_matrix(y_test, y_pred)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    logit_roc_auc = roc_auc_score(y_test, logreg.predict(x_test[xColsToKeep]))
    fpr, tpr, thresholds = roc_curve(
        y_test, logreg.predict_proba(x_test[xColsToKeep])[:, 1]
    )
    #    plt.figure()
    plt.plot(fpr, tpr, label=runName + " (area = %0.2f)" % logit_roc_auc)
    plt.plot([0, 1], [0, 1], "r--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver operating characteristic")
    plt.legend(loc="lower right")
    plt.savefig("Log_ROC")


#    plt.show()


def runAll(doOverSample, doRFE, numColsToKeep=0):
    print(
        "Running logistic regression",
        "with oversampling" if doOverSample else "",
        f"with RFE with {numColsToKeep} cols" if doRFE else "",
    )
    runName = "LR"
    os_data_x, os_data_y, x_train, x_test, y_train, y_test = overSample(x, y)
    if doOverSample:
        x_train = os_data_x
        y_train = os_data_y
        runName += "_OS"
    if doRFE:
        xColsToKeep = recursiveFE(numColsToKeep, x_train, y_train)
        runName += "_RFE" + str(numColsToKeep)
    else:
        xColsToKeep = xCols
    fitLogRegModel(x_train, y_train, x_test, y_test, xColsToKeep, runName)


plt.figure(figsize=(15, 11))
for os in [True, False]:
    for rfe in [True, False]:
        for i,num in enumerate([5, 10, 15, 20, 25, 30]):
            runAll(os, rfe, num)
            if (i>0) and (rfe == False):
                break # stop it doing the same thing 5x if RFE not used
#runAll(True, True, 20)
#runAll(False, False)
#runAll(True, False)
#runAll(False, True, 20)
#runAll(True, True, 10)
plt.show()
#
#
# clf = LogisticRegression(solver="lbfgs").fit(x, y)
#
# pred = clf.predict(x)
# prob = clf.predict_proba(x.iloc[:numberToTry, :])
#
##for example in range(numberToTry):
##    print(y.iloc[example], pred[example])
#
# print(confusion_matrix(y, pred))
