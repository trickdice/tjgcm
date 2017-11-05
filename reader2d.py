''' Author @HXT'''
from copy import copy
import MITgcmutils as mit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

print 'reading files...\nXC/YX/W/hFacC/Depth'
# MAXTIME = float(raw_input("input the maximun iteration:\n"))
# read data
singleiter = 150000
# temperature
T = mit.rdmds('T', singleiter)
DEPTH = mit.rdmds('Depth')
TOPO = mit.rdmds('hFacC')
XC = mit.rdmds('XC')
(NZ, NY, NX) = np.shape(T)
# DELT = MAXTIME/(ITS-1)
CLB_MAX = np.max(T)# color bar
CLB_MIN = np.min(T)
if CLB_MIN == 0:
    CLB_MIN = np.min(T[:, 0, 0])
T0 = np.reshape(T[:, 0, :], (NZ, NX))
# velocity
U = mit.rdmds('U', singleiter)
W = mit.rdmds('W', singleiter)
U0 = np.reshape(U[:, 0, :], (NZ, NX))
W0 = np.reshape(W[:, 0, :], (NZ, NX))

# FIGURE-------------------------

xaxis = np.arange(0.0,NX,1.0)
zaxis = np.arange(0.0,NZ,1.0)
# basic temperatue
NORM = mpl.colors.Normalize(vmin=CLB_MIN-0.2, vmax=CLB_MAX)
mycmap = copy(plt.cm.jet)
mycmap.set_under('b',1.0)
fig, ax = plt.subplots()
im = ax.imshow(T0, interpolation='bilinear',
                cmap=mycmap,
                norm=NORM,
                aspect='auto')
cbar = fig.colorbar(im, extend='both', shrink=0.9, ax=ax)
cbar.set_label('Temperature /$^\circ$C')

# draw topography
ztopo = np.reshape(DEPTH,[NX])/(DEPTH[0,0]/NZ)
zbase = NZ*np.ones(NX)
ax.fill_between(xaxis, ztopo, zbase, where=ztopo<zbase, facecolor='gray')

# lables
plt.title('ISWs over Sanddunes')
plt.xlabel('Distance /km') # x-axis
plt.xlim(0, NX-1)
plt.xticks(np.linspace(0, NX-1, 7), \
    np.linspace(0, XC[0, -1]+XC[0, 1], 7)/1000)
plt.ylabel('Depth /km') # y-axis
plt.ylim(NZ-1, 0)
plt.yticks(np.linspace(NZ-1, 0, 6), \
    np.linspace(DEPTH[0, 0], 0, 6))

# velocity quiver
bleft,bright,btop,bbuttom = 50,205,40,160
q = ax.quiver(xaxis[bleft:bright:5], zaxis[btop:bbuttom:5], U0[btop:bbuttom:5,\
              bleft:bright:5], W0[btop:bbuttom:5,bleft:bright:5])
# ax.quiverkey(q, xaxis[::5], zaxis[::5], U=1)


plt.show()