# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:24:15 2017

@author: HXT
"""
from __future__ import division
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.colors import LightSource
import os
from scipy import interpolate
import sys
import numpy as np
import matplotlib.pyplot as plt
""" Functions"""
# write single file
def dltf(fname):
    if os.path.exists(fname):
        print 'deleting original ', fname, '...'
        os.remove(fname)
def writebin(fname, bindata):
    print 'write to file: '+fname
    if sys.byteorder == 'little':
        bindata.byteswap(True)
    fid = open(fname, 'wb')
    bindata.tofile(fid)
    fid.close()
# write to data file
def writetxt(fname, txtdata):
    fid = open(fname, 'a+')
    fid.write(txtdata)
    fid.close()
# add one dune to the topography
def addd(ny,nx,cenx,ceny,d_w,d_h):
    topomask = np.zeros((ny,nx),dtype='float64')
    if (d_w%2) == 0:
        d_w = d_w-1
        print 'moved the dune to suit the grid'
    if (cenx-d_w/2 < 0) or (cenx+d_w/2+1 >= nx) or \
    (ceny-d_w/2 < 0) or (ceny+d_w/2+1 >= ny):
        print 'exceeds boundary!!!!'
    X = np.arange(-d_w/2, d_w/2, 1)
    Y = np.arange(-d_w/2, d_w/2, 1)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    b, c = 1,1
    nnn = (R-b)**2/(2*c**2)
    dunex = d_h*np.exp(-nnn)
    yb1 = int(ceny-d_w/2-0.5)
    yb2 = int(ceny+d_w/2-0.5)
    xb1 = int(cenx-d_w/2-0.5)
    xb2 = int(cenx+d_w/2-0.5)
    topomask[yb1:yb2,xb1:xb2] += dunex
    return topomask
"""Generate data"""
# grid // space // norms
nx, ny,nz = 80, 60, 100
lx, ly, lz = 1.6*pow(10,4), 1.2*pow(10,4), 400 
gravity, talpha, n2 = 9.81, 2*pow(10,-4), pow(10,-6)
# Resolution
dx=np.arange(nx,dtype='float64')
for i in np.arange(nx):
    i = int(i)
    dx[i] = lx/(nx+1)
dy=np.arange(ny,dtype='float64')
for i in np.arange(ny):
    i = int(i)
    dy[i] = ly/(ny+1)
dz=np.arange(nz,dtype='float64')
for i in np.arange(nz):
    i = int(i)
    dz[i] = lz/(nz+1)
print('delZ=%5.1f * %5.1f'%(nz,dz[0]))

x = np.arange(nx)
x[0] = dx[0]
for i in np.arange(nx-1):
    i = int(i)
    x[i+1] = x[i]+dx[i+1]
# Stratification
# fake
# ---real---
tmp = np.loadtxt('tempx.txt')
k = np.shape(tmp)
for i in range(k[0]):
    if tmp[i][0] > lz:
        break
i = i+2
tmpx = tmp[0:i]
dpthse = np.linspace(1,lz,nz)
fitplt = interpolate.interp1d(tmpx[:,0],tmpx[:,1],kind = "cubic")
tmpse = fitplt(dpthse)
plt.figure(1) # temperature profile
plt.plot(tmpse)
plt.grid()
# write to tref.txt
fname = 'txtemperature.txt'
dltf(fname)
for i in range(0,nz-1,4):
    writetxt(fname,'        ')
    writetxt(fname,"{0:.6f},{0:.6f},{0:.6f},{0:.6f},\n".format(tmpse[i],\
             tmpse[i+1],tmpse[i+2],tmpse[i+3]))
# T.init
tint = np.zeros([nz,ny,nx],dtype='float64')
for i in range(nz):
    tint[i,:,:] = tmpse[i]
# design topo-----------------------------------------
# basic topography
d = np.ones((ny,nx),dtype='float64')
d = -lz*d
d[:,nx-1] = 0

# add background slope
dip = 0.02;
dip = dip*dx[0]
for i in range(0,nx-1,1):
    d[:,i] = d[:,i]+dip*i

# add dunes
# addd(ny,nx,cenx,ceny,d_w,d_h)
d = d+addd(ny,nx,20,20,5,20)
d = d+addd(ny,nx,30,20,5,20)

plt.figure(2)   # topography-2d
plt.plot(d[0,:])
plt.xlabel('x')
plt.ylabel('z')

plt.figure(3)   # topography-upside
plt.imshow(d)
plt.xlabel('x')
plt.ylabel('y')

fig, ax = plt.subplots()  # topography-3d
ax = fig.add_subplot(1, 1, 1, projection='3d')
X = np.arange(0, nx, 1.0)
Y = np.arange(0, ny, 1.0)
X, Y = np.meshgrid(X, Y)

ls = LightSource(270, 45)
rgb = ls.shade(d, cmap=cm.copper, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(X, Y, d, rstride=1, cstride=1, facecolors=rgb,
        linewidth=0, antialiased=False)
ax.view_init(azim=240)

# design slope-----------------------------------------
# tintx = np.reshape(tint,[nz,ny,nx])
if np.max(d)>0:
    print 'Higher than 0!!!!!!'
plt.figure(3)


# write slope

dltf('topog.slope')
writebin('topog.slope',d)
dltf('delXvar')
writebin('delXvar',dx)
dltf('delYvar')
writebin('delYvar',dy)
dltf('delZvar')
writebin('delZvar',dz)
dltf('T.init')
writebin('T.init',tint)


print('end of generating data...')
plt.show()

# 19.49?
# is that all?
