# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:47:51 2019

@author: reesc1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

################# ADD MORE FEATURES TO INPUT DATA ###############################
dfIn = pd.read_csv("clusterDF.csv")
dfIn.drop("Unnamed: 0", inplace=True, axis=1)
originalCols = ["no insps", "insp n", "insp n-1", "insp n-2", "insp n-3", "insp n-4..0"]
dfInT = pd.DataFrame(dfIn.values.transpose(), columns=originalCols)
# MAKE INSPECTION CATS BINARY
for col in set(dfInT.columns) - {"no insps"}:
    dfInT[col] = np.where((dfInT[col].isin([1, 2])), 1, 0)
dfInT["Change 1"] = dfInT["insp n"] - dfInT["insp n-1"]
dfInT["Change 2"] = dfInT["insp n"] - dfInT["insp n-2"]
dfInT["Change 3"] = dfInT["insp n"] - dfInT["insp n-3"]
dfInT["Change 23"] = dfInT["insp n-1"] - dfInT["insp n-2"]
dfInT["Change 34"] = dfInT["insp n-2"] - dfInT["insp n-3"]
originalCols = dfInT.columns


################# DOING THE PCA ##################################################
# dfIn = pd.read_csv("clusterDF.csv")
# dfIn.drop('Unnamed: 0', inplace=True, axis=1)
x = dfInT.values
x = StandardScaler().fit_transform(x)


def doPCA(numPCs=6):
    pca = PCA(n_components=numPCs)
    PCs = pca.fit_transform(x)
    print(pca.explained_variance_ratio_, "with", numPCs, "components")
    print(np.cumsum(pca.explained_variance_ratio_), "<- cumsum of explained variance")

    newDFwithPCs = pd.DataFrame(
        data=PCs,
        columns=["principal component " + str(x) for x in list(range(1, numPCs + 1))],
    )

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("Principal Component 1", fontsize=15)
    ax.set_ylabel("Principal Component 2", fontsize=15)
    ax.set_title("2 component PCA - plotting the points", fontsize=20)
    # targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    # colors = ['r', 'g', 'b']
    # for target, color in zip(targets,colors):
    #    indicesToKeep = finalDF['target'] == target
    ax.scatter(
        newDFwithPCs.loc[:, "principal component 1"],
        newDFwithPCs.loc[:, "principal component 2"],
        s=50,
    )
    # ax.legend(targets)
    ax.grid()
    return newDFwithPCs


##################### CLUSTERING ON ORIGINAL DATA ########################################################
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc


def doClustering():
    finalDF = newDFwithPCs[:]
    plt.figure(figsize=(10, 7))
    plt.title("Dendograms")
    dend = shc.dendrogram(shc.linkage(x, method="ward"))

    for numClusters in [2, 3, 4, 5, 6, 7]:
        cluster = AgglomerativeClustering(n_clusters=numClusters)
        a = cluster.fit_predict(x)

        finalDF = pd.concat(
            [finalDF, pd.Series(a, name=f"Cluster{numClusters}")], axis=1
        )
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel("Principal Component 1", fontsize=15)
        ax.set_ylabel("Principal Component 2", fontsize=15)
        ax.set_title(f"{numClusters} clusters plotted PC1 vs PC2", fontsize=20)
        targets = list(range(numClusters))
        colours = ["r", "g", "b", "k", "y", "c", "m"]
        for target, colour in zip(targets, colours[:numClusters]):
            indicesToKeep = finalDF[f"Cluster{numClusters}"] == target
            ax.scatter(
                newDFwithPCs.loc[indicesToKeep, "principal component 1"],
                newDFwithPCs.loc[indicesToKeep, "principal component 2"],
                c=colour,
                s=50,
            )
        ax.legend(targets)
        ax.grid()
    return finalDF


################### INTERPRET CLUSTERING RESULTS #######################################################
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


def interpretClusters(dfInT, finalDF):
    #    dfIn = pd.read_csv("clusterDF.csv")
    #    dfIn.drop('Unnamed: 0', inplace=True, axis=1)
    #    originalCols = ['no insps','insp n','insp n-1', 'insp n-2','insp n-3','insp n-4..0']
    #    dfInT = pd.DataFrame(dfIn.values.transpose(),columns = originalCols)
    dfDataPCsClusters = pd.concat([dfInT, finalDF], axis=1)

    for numClusters in range(2, 8):
        for col in originalCols:
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(1, 1, 1)
            #    ax.set_xlabel('Principal Component 1', fontsize = 15)
            #    ax.set_ylabel('Principal Component 2', fontsize = 15)
            ax.set_title(f"{col} with {numClusters} clusters", fontsize=20)
            targets = list(range(numClusters))
            colours = ["r", "g", "b", "k", "y", "c", "m"]
            for target, colour in zip(targets, colours[:numClusters]):
                indicesToKeep = dfDataPCsClusters[f"Cluster{numClusters}"] == target
                ax.hist(
                    dfDataPCsClusters.loc[indicesToKeep, col],
                    alpha=0.8,
                    rwidth=0.8
                    #                    histtype = 'step'
                    #                       c=colour,
                    #                        s = 50
                )
            ax.legend(targets)
            ax.grid()


################# RUN IT ######################################################################
newDFwithPCs = doPCA(6)
finalDF = doClustering()
interpretClusters(dfInT, finalDF)
