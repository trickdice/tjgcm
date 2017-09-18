# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:24:15 2017

@author: HXT
"""
from __future__ import division
from scipy import interpolate
import sys
import numpy as np
""" Functions"""
# write single file
def writesinglefile(fname,data):
    print('write to file: '+fname)
    if sys.byteorder == 'little':
        data.byteswap(True)
    fid = open(fname,"wb")
    data.tofile(fid)
    fid.close
# write to data file
def writedata(xindata):
    nindata=open("data","w")
    nindata.write(xindata)
    nindata.close()
def appenddata(xindata):
    nindata=open("data","a+")
    nindata.write(xindata)
    nindata.close()
"""Generate data"""
# grid // space // norms
nx, ny,nz = 1100.0, 1.0, 400.0
lx, h = 4.4*pow(10,4), 400 
gravity, talpha, n2 = 9.81, 2*pow(10,-4), pow(10,-6)
# Resolution
dx=np.arange(nx)
for i in np.arange(nx):
    i = int(i)
    dx[i] = lx/(nx+5)
dy = lx/nx
dz = h/nz
print('delZ={0:4.4} * {1:3.3}'.format(nz,dz))

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
# real
tmp = np.loadtxt('tempx.txt')
k = np.shape(tmp)
for i in range(k[0]):
    if tmp[i][0] > h:
        break
i = i+2
tmpx = tmp[0:i]
dpthse = np.linspace(0,400,401)
tmpse = np.interp(dpthse.tolist(),tmpx[:,0].tolist(),tmpx[:,1].tolist())
"""
fresample = interpolate.interp1d(tmpx[:,0],tmpx[:,1],kind='cubic')
dpthse = np.arange(400)+1
tmpse = fresample(dpthse)
"""
print('total depth is',h,'in  grid',nz)   
fname = 'stratification.bin'
writesinglefile(fname,tmpse)

# write to data file
"""Write initial text to data"""
writedata("# ===================="+'\n'\
          +"# | Model parameters |"+"\n"\
          +"# |   @author: HXT   |"+"\n"\
          +"# ===================="+"\n"\
          +"#"+"\n"\
          +"# Continuous equation parameters"+"\n"\
          +" &PARM01"+"\n")
appenddata("Tref = ")
appenddata("")