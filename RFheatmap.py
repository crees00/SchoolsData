# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:11:10 2019

@author: Chris
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from os import listdir
import setFolder as sf

df = pd.read_csv('fullBashsep8SFS2ColsAdded.csv')

RFs = df[df['RF']==1]
maxX = int(max(RFs['p2']))
maxY = int(max(RFs['p3']))
RFsNoEdges = RFs[RFs['p2']>22]
RFsNoEdges = RFsNoEdges[RFsNoEdges['p3']>2]

#plt.scatter(RFsNoEdges['p2'], RFsNoEdges['p3'], c=RFsNoEdges['acc'], cmap='magma',s=1)

avgs = pd.DataFrame(np.zeros((maxY+1, maxX+1)))
avgs.drop(0, inplace=True)
avgs.drop(0, inplace=True, axis=1)

step=1
for x in range(1,50):#maxX+1, step):
    for y in range(1,50):#maxY+1,step):
        RFsubset = RFs[(RFs['p2'] >= x) & (RFs['p2'] < (x+step))]
        RFsubset = RFs[(RFs['p3'] >= y) & (RFs['p3'] < (y+step))]
        score = RFsubset['auc'].mean()
#        print(x,y,score)
#        print(RFsubset['auc'].head())
        for i in range(step):
            for j in range(step):
                avgs.loc[y+i,x+j] = score#RFsubset['auc'].mean()



# generate 2 2d grids for the x & y bounds
y, x = np.meshgrid(np.linspace(1, maxY, maxY), np.linspace(1, maxX, maxX))

z = avgs.values
z=z.T
# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
z = z[:-1, :-1]
z_min, z_max = np.abs(z).min(), np.abs(z).max()

fig, ax = plt.subplots()

c = ax.pcolormesh(x, y, z, cmap='RdBu')#, vmin=z_min, vmax=z_max)
ax.set_title('pcolormesh')
# set the limits of the plot to the limits of the data
ax.axis([x.min(), x.max(), y.min(), y.max()])
fig.colorbar(c, ax=ax)

plt.show()