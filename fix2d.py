# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:24:15 2017

@author: HXT
"""
from __future__ import division
import os
from scipy import interpolate
import sys
import numpy as np
'''import pylab as pl'''
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
"""Generate data"""
# grid // space // norms
nx, ny,nz = 300, 1, 200
lx, h = 3.0*pow(10,4), 400 
gravity, talpha, n2 = 9.81, 2*pow(10,-4), pow(10,-6)
# Resolution
dx=np.arange(nx)
for i in np.arange(nx):
    i = int(i)
    dx[i] = lx/(nx+1)
dy = lx/nx
dz = h/nz
print('delZ=%5.1f * %5.1f'%(nz,dz))

x = np.arange(nx)
x[0] = dx[0]
for i in np.arange(nx-1):
    i = int(i)
    x[i+1] = x[i]+dx[i+1]

z = -dz*np.arange(h//dz)-dz/2
# Stratification
# fake
tz = n2/(gravity*talpha)
tref = tz*(z-z.mean())
# ---real---
tmp = np.loadtxt('tempx.txt')
k = np.shape(tmp)
for i in range(k[0]):
    if tmp[i][0] > h:
        break
i = i+2
tmpx = tmp[0:i]
dpthse = np.linspace(1,h,nz)
fitplt = interpolate.interp1d(tmpx[:,0],tmpx[:,1],kind = "cubic")
tmpse = fitplt(dpthse)
plt.figure(1)
plt.plot(tmpse)
plt.grid()
# write to tref.txt
fname = 'txtemperature.txt'
dltf(fname)
for i in range(0,nz-1,4):
    writetxt(fname,'        ')
    writetxt(fname,"{0:.6f},{0:.6f},{0:.6f},{0:.6f},\n".format(tmpse[i],\
             tmpse[i+1],tmpse[i+2],tmpse[i+3]))
# write to T.init
tint = np.zeros([nz,ny,nx])
for i in range(nz):
    tint[i,:,:] = tmpse[i]
# design slope
d = np.ones((nx))
d = -h*d
d[nx-1] = 0
dip = 0.015
for i in range(30,nx-1,1):
    d[i] = (i-30)*dip*dx[0]-h
d[260:nx-2] = -58
plt.figure(2)
plt.plot(d)
plt.grid()
# write slope
tintx = np.reshape(tint,[nz,nx])
plt.imshow(tintx, cmap='jet')

dltf('topog.slope')
writebin('topog.slope',d)
dltf('delXvar')
writebin('delXvar',dx)
dltf('T.init')
writebin('T.init',tint)




print('end of generating data...')
plt.show()

# 19.49?
# is that all?
