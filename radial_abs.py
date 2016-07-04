#!/usr/bin/env python

import numpy as np

data = np.loadtxt("./U_0allf.dat",skiprows=2)

rads = data[:,0]
thetas = data[:,1]
phis = data[:,2]
Uabss = data[:,3]

npts = np.max(rads.shape)

result = 0

ct = 0

#for i in range(npts-1):
  #rn = rads[i]
  #rnp1 = rads[i+1]
  #r = 0.5*(rn+rnp1)
  #dr = rnp1-rn
  #for j in range(npts-1):
    #thn = thetas[i]
    #thnp1 = thetas[i+1]
    #sthdth = np.sin(0.5*(thnp1+thn))*(thnp1-thn)
    #for k in range(npts-1):
      #phn = phis[i]
      #phnp1 = phis[i+1]
      #dph = phnp1 - phn
      #result += Uabss[ct]*r*r*dr*sthdth*dph
      #ct += 1
      
for i in range(npts-1):
  rn = rads[i]
  rnp1 = rads[i+1]
  r = 0.5*(rn+rnp1)
  dr = rnp1-rn
    
  thn = thetas[i]
  thnp1 = thetas[i+1]
  sthdth = np.sin(0.5*(thnp1+thn))*(thnp1-thn)
  
  phn = phis[i]
  phnp1 = phis[i+1]
  dph = phnp1 - phn
  
  result += Uabss[i]*r*r*dr*sthdth*dph
      
print "Gods be good: " + str(result)
