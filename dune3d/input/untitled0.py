#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 21:44:48 2017

@author: cary
"""

# from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax = fig.add_subplot(1, 1, 1, projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
a, b, c = 1,1,1
nnn = (R-b)**2/(2*c**2)
Z = a*np.exp(-nnn)
# Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.gist_earth,
        linewidth=0, antialiased=False)
#ax.set_zlim3d(-1.01, 1.01)

#ax.w_zaxis.set_major_locator(LinearLocator(10))
#ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

plt.show()