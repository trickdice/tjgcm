import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# picks topography-2d only
im = Image.open("D84rb.tif")
fig, ax = plt.subplots()
im = ax.imshow(im, interpolation='bilinear',
                aspect='auto')
#-------------------------
#-------------------------
# on z axis
zp = [0,1.7]
# on x axis
xp = [16000,0]
#-------------------------
#-------------------------
strx = raw_input('ready for pick z axis?   y/n\n')
if strx=='y':
    print 'end input with enter'
    pickerz = plt.ginput(3)
    z0 = np.array(pickerz[0])
    z1 = np.array(pickerz[1])
    z2 = np.array(pickerz[2])
    z = (z1+z2+z0)/3
#------------------------
strx = raw_input('ready for pick x axis?   y/n\n')
if strx=='y':
    print 'end input with enter'
    pickerx = plt.ginput(3)
    x0 = np.array(pickerx[0])
    x1 = np.array(pickerx[1])
    x2 = np.array(pickerx[2])
    x = (x0+x1+x2)/3
#---------------------
# trans axis-dist/dept
k_x = (xp[0]-zp[0])*6.25/(x[0]-z[0])
k_z = (zp[1]-xp[1])*750/(z[1]-x[1])
#-------------------------
strx = raw_input('ready for pick? y/n\n')
if strx=='y':
    print 'end input with enter'
    pickertopo = plt.ginput(500)
    pickertopo = np.array(pickertopo)
for i in range(np.shape(pickertopo)[0]):
    pickertopo[i,0] = (pickertopo[i,0]-x[0])*k_x+xp[0]*6.25
    pickertopo[i,1] = (pickertopo[i,1]-z[1])*k_z+zp[1]*750
# xxx = np.vstack((z,x,pickertopo))
