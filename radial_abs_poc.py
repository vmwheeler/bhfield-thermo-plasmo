#!/usr/bin/env python

import numpy as np

nr=130
nth=130
nph=130
rads = np.linspace(0,1,nr)
thetas = np.linspace(0,np.pi,nth)
phis = np.linspace(0,2*np.pi,nph)

print "total number of points: " + str(nr*nth*nph)

radshell = np.max(rads)  

npts = np.max(rads.shape)

result = 0
           
rold = 0
thold = 0
phold = 0
vol = 0

dth = thetas[1]
dph = phis[1]
dr = rads[1]

for rad in rads:
  #print "new rad"
  #dr = rad - rold
  #rold = np.copy(rad)
  for i in range(len(thetas)-1):
    
    #sinthdth = np.cos(thold) - np.cos(theta)
    #sinthdth = np.sin(0.5*(thetas[i+1]+thetas[i]))*dth
    sinthdth = np.sin(thetas[i])*dth
    #print sinthdth
    #phold = 0
    for phi in phis:
      #print "rad: " + str(rad) 
      #print "dr: " + str(dr)
      #print "dth: " + str(dth)
      #print "dph: " + str(dph)
      vol += rad*rad*dr*sinthdth*dph
      
  
realvol = 4./3.*np.pi*radshell**3.
print "volume check (" + str(realvol) + "): " + str(vol)  
#print "Gods be good: " + str(result)


###!/usr/bin/env python

#from scipy.integrate import quad, dblquad, tplquad
#import numpy as np
## limits for radius
#r1 = 0.
#r2 = 1.
## limits for theta
#t1 = 0
#t2 = 2*np.pi
## limits for phi
#p1 = 0
#p2 = np.pi

#def diff_volume(p,t,r):
    #return r**2*np.sin(p)

#volume = tplquad(diff_volume, r1, r2, lambda r:   t1, lambda r:   t2,
                                      #lambda r,t: p1, lambda r,t: p2)[0]

#print 4./3.*np.pi*r2**3.
#print volume
