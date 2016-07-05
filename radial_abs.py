#!/usr/bin/env python

import numpy as np
#import matplotlib.pyplot as plt

data = np.loadtxt("./U_0allf.dat",skiprows=2)

rads = data[:,0]
rads = rads/np.max(rads)
thetas = data[:,1]
phis = data[:,2]
Uabss = data[:,3]

#rads = np.linspace(0.0000,1.,30)
#thetas = np.linspace(0,np.pi,40)
#phis = np.linspace(0,2*np.pi,70)


radshell = np.max(rads)  

npts = np.max(rads.shape)

result = 0

ct = 0
           
dr = rads[0]
rad = rads[0]
avrad = 0.5*rad
          
dth = phis[1] - phis[0]
dph = phis[1] - phis[0]

print "rad: " + str(rad) 
print "dr: " + str(dr)
print "dth: " + str(dth)
print "dph: " + str(dph)

vol = 0    
for i in range(npts):
  
  if rads[i]>rad:
    rad = rads[i]
    dph = phis[i+1] - phis[i]
    dth = np.copy(dph)
    print dth
    print dph
    
  dV = rad*rad*np.sin(thetas[i])*dth*dph


  #result += Uabss[i]*rad*rad*dr*sinthdth*dph
  vol += dV
  #vol += avrad**2.*dr*sinthdth*dph
  
realvol = 4./3.*np.pi*radshell**3.
print "volume check (" + str(realvol) + "): " + str(vol)  
#print "Gods be good: " + str(result)
