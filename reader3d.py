''' Author @HXT'''
from copy import copy
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.colors import LightSource
import MITgcmutils as mit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

print 'reading files...\nXC/YX/W/hFacC/Depth'
# MAXTIME = float(raw_input("input the maximun iteration:\n"))
# read data
coco = 10

singleiter = 0
# temperature
data = mit.rdmds('T', singleiter)
DEPTH = mit.rdmds('Depth')
TOPO = mit.rdmds('hFacC')
XC = mit.rdmds('XC')
(NZ, NY, NX) = np.shape(data)
# DELT = MAXTIME/(ITS-1)
CLB_MAX = np.max(data)# color bar
CLB_MIN = np.min(data)
if CLB_MIN == 0:
    CLB_MIN = np.min(data[:, 0, 0])
if NY == 1:
    datain = np.reshape(data[:, 0, :], (NZ, NX))
else:
    datain = data

# surface--------------
xaxis = np.arange(0.0,NX,1.0)
yaxis = np.arange(0.0,NY,1.0)
zmap = np.zeros([NY,NX])


for j in np.arange(NY):
    for i in np.arange(NX):
        dtmp = datain[:,j,i]
        ztmp = np.argwhere(np.abs(dtmp-coco)==np.min(np.abs(dtmp-coco)))
        if np.size(ztmp)>1:
            ztmp = np.max(ztmp)
        zmap[j,i] = -int(ztmp)
zmap[:,0] = -np.max(NZ)
zmap[:,NX-1] = 0
plt.figure()
fig, ax = plt.subplots()  # topography-3d
ax = fig.add_subplot(1, 1, 1, projection='3d')
xaxis, yaxis = np.meshgrid(xaxis, yaxis)

ls = LightSource(270, 45)
rgb = ls.shade(zmap, cmap=cm.jet, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(xaxis, yaxis, zmap, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False)
ax.view_init(azim=240)
plt.xlabel('South-North')
plt.ylabel('East-West')
plt.show()
