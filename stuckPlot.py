# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:04:49 2019

@author: reesc1
"""

import matplotlib.pyplot as plt
import numpy as np

# here's our data to plot, all normal Python lists
x = [x - 0.5 for x in list(range(6))]
y = [x - 0.5 for x in list(range(9))]

intensity = finalPt

# setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

# convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(intensity)

# now just plug the data into pcolormesh, it's that easy!
fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(5)
a = ax.pcolormesh(x, y, intensity)
fig.suptitle("Frequencies of inspection history")
ax.set_xlabel("Total good (cat1/cat2) inspections")
ax.set_ylabel("Total bad (cat3/cat4) inspections")
plt.colorbar(a) #need a colorbar to show the intensity scale
plt.show()  # boom
