# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:47:51 2019

@author: reesc1
"""
import setFolder as sf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
#sns.set()
################# ADD MORE FEATURES TO INPUT DATA ###############################
dfIn = pd.read_csv(sf.addFolderPath("bbbbVgsbbbsAllCols.csv"))
dfIn.drop(["Unnamed: 0","Unnamed: 0.1"], inplace=True, axis=1)
originalCols = dfIn.columns
#print(originalCols)
#dfInT = pd.DataFrame(dfIn.values.transpose(), columns=originalCols)
# MAKE INSPECTION CATS BINARY
#originalCols = dfInT.columns


################# DOING THE PCA ##################################################
# dfIn = pd.read_csv("clusterDF.csv")
# dfIn.drop('Unnamed: 0', inplace=True, axis=1)
x = dfIn.drop(['URN','Class'], axis=1).values
#x = dfIn.values
x = dfIn.drop([747])
x = StandardScaler().fit_transform(x)


def doPCA(numPCs=6):
    pca = PCA(n_components=numPCs)
    PCs = pca.fit_transform(x)
    print(pca.explained_variance_ratio_, "with", numPCs, "components")
    print(np.cumsum(pca.explained_variance_ratio_), "<- cumsum of explained variance")
    
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    plt.grid()
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
###################################################################################
def plotClassesOnPCA(newDFwithPCs):
    
    newDFwithPCs = newDFwithPCs.join(other=dfIn.drop([747])[['Class','URN']])
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("Principal Component 1", fontsize=15)
    ax.set_ylabel("Principal Component 2", fontsize=15)
    ax.set_title("Comparison of the two classes using PCA\nUpdated definition of stuck", fontsize=20)
    ax.set_ylim([-7,15])
    ax.scatter(
        newDFwithPCs[newDFwithPCs['Class']==1].loc[:, "principal component 1"],
        newDFwithPCs[newDFwithPCs['Class']==1].loc[:, "principal component 2"],
        s=2,
        c='r'
    )
    ax.scatter(
        newDFwithPCs[newDFwithPCs['Class']==0].loc[:, "principal component 1"],
        newDFwithPCs[newDFwithPCs['Class']==0].loc[:, "principal component 2"],
        s=2,
        c='c'
    )
    ax.legend(['Stuck','Escaped Stuck'],loc='lower right', fontsize='large')
    # ax.legend(targets)
#    ax.grid()
################# RUN IT ######################################################################
newDFwithPCs = doPCA(60)
#finalDF = doClustering()
#interpretClusters(dfIn, finalDF)
plotClassesOnPCA(newDFwithPCs)
