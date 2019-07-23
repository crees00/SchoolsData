# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:47:51 2019

@author: reesc1
"""

import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

x = pd.read_csv('clusterDF.csv')
x = x.to_numpy().transpose()
cluster = AgglomerativeClustering(n_clusters=2)
cluster.fit_predict(x)


import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("Dendograms")
dend = shc.dendrogram(shc.linkage(x, method='ward'))


plt.figure(figsize=(10, 7))
plt.scatter( x[:,1],x[:,4], c=cluster.labels_, cmap='rainbow')