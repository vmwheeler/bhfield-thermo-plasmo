#!/usr/bin/env python
import numpy as np
from scipy.integrate import quad, dblquad, tplquad, nquad
from scipy.interpolate import griddata, LinearNDInterpolator
from math import isnan
import matplotlib.pyplot as plt
#from mayavi import mlab

data = np.loadtxt("./U_0allf_rad.dat",skiprows=2)

radshell = 0.06  
radcore = radshell/2.

#global Uabss
Uabss = data[:,3]

#global pts
pts = data[:,0:3]

ct = 0



interp = LinearNDInterpolator(pts,Uabss)

#xs = np.linspace(-radshell,radshell,100)
#ys = np.linspace(-radshell,radshell,100)
#zs = np.linspace(-radshell,radshell,100)

xx,yy = np.mgrid[-radshell:radshell:0.0005,-radshell:radshell:0.0005]

#print xx
#print yy

interpslice = lambda x,y: interp(x,0.0,y)

mlab.surf(xx,yy,interpslice)
mlab.show()

#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.36960E+01),method='linear')
#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.377E+01),method='linear')
#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.38808E+01),method='linear')

npts = np.max(Uabss.shape)

pi = np.pi

# limits for radius
r1 = 0.
r2 = radcore
r3 = radshell
# limits for theta
t1 = 0.
t2 = np.pi
# limits for phi
p1 = 0.
p2 = 2.*np.pi


def diff_volume(p,t,r):
  return r**2*np.sin(t)

  out = griddata(pts,Uabss,(r,t,p),method='linear')*r**2*np.sin(t)
  print out
  if isnan(out):
    print 'oh fuck'
    die
  else:
    return out
  
def new_diff_Uabs(p,t,r):
  out = interp(r,t,p)*r**2.*np.sin(t)
  #out = r**(1.22)*r**2.*np.sin(t)
  #print out
  if isnan(out):
    print 'oh fuck'
    die
  else:
    return out

volume = tplquad(diff_volume, r1, r3, lambda r:   t1, lambda r:   t2,
                                      lambda r,t: p1, lambda r,t: p2)[0]
print 'volume check (' + str(4./3.*np.pi*(r3)**3.) + '): ' + str(volume)


Qabs = tplquad(new_diff_Uabs, r1, r3, lambda r:   t1, lambda r:   t2,
                                      lambda r,t: p1, lambda r,t: p2,
                                      epsabs=1.49e-04, epsrel=1.49e-04)[0]
print 'Qabs_core: ' + str(Qabs_core)
#Qabs_shell = tplquad(diff_Uabs, r2, r3, lambda r:   t1, lambda r:   t2,
#                                      lambda r,t: p1, lambda r,t: p2)[0]
#print 'Qabs_shell: ' + str(Qabs_shell)
#print 'Qabs (0.65...): ' + str(Qabs_core + Qabs_shell)
#Qabs = tplquad(diff_Uabs, r1, r3, lambda r:   t1, lambda r:   t2,
#                                        lambda r,t: p1, lambda r,t: p2)[0]

#print Qabs
