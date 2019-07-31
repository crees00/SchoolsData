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

intensity = steps

# setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

# convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(intensity)

# now just plug the data into pcolormesh, it's that easy!
fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(5)
ax.pcolormesh(x, y, intensity)
fig.suptitle("Steps along the way")
ax.set_xlabel("Total goods")
ax.set_ylabel("Total bads")
# fig.colorbar() #need a colorbar to show the intensity scale
plt.show()  # boom
