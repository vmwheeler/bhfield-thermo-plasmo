#!/usr/bin/env python
import numpy as np
from scipy.integrate import quad, dblquad, tplquad, nquad
from scipy.interpolate import griddata, LinearNDInterpolator, Rbf
from math import isnan
import matplotlib.pyplot as plt
from mayavi import mlab

data = np.loadtxt("./U_0allf_cart.dat",skiprows=2)

radshell = 0.06E-6
radcore = radshell/2.

#global Uabss
Uabss = data[:,3]

#global pts
pts = data[:,0:3]*1E-6

print pts

ct = 0

interp = Rbf(pts[:,0],pts[:,1],pts[:,2],Uabss)


#xs = np.linspace(-radshell,radshell,100)
#ys = np.linspace(-radshell,radshell,100)
#zs = np.linspace(-radshell,radshell,100)

xx,yy = np.mgrid[-radshell:radshell:0.001,-radshell:radshell:0.001]

#print xx
#print yy

def interpslice(q1,q2):
  zshape = np.shape(q2)
  zeerho = np.zeros(zshape)
  return interp(q1,q2,zeerho)



#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.36960E+01),method='linear')
#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.377E+01),method='linear')
#print griddata(pts,Uabss,(0.27273E-01,  0.18480E+01,  0.38808E+01),method='linear')

npts = np.max(Uabss.shape)

pi = np.pi

# limits for x
x1 = -radshell
x2 = radshell
# limits for y
y1 = -radshell
y2 = radshell
# limits for z
z1 = -radshell
z2 = radshell


#Qabs = tplquad(new_diff_Uabs, r1, r3, lambda r:   t1, lambda r:   t2,
#                                      lambda r,t: p1, lambda r,t: p2,
#                                      epsabs=1.49e-04, epsrel=1.49e-04)[0]
Uabs_T = tplquad(interp,x1,x2, lambda x: y1, lambda x: y2,
                             lambda x,y: z1, lambda x,y: z2)

Ap = np.pi*radshell*radshell
print 'Uabs_T: ' + str(Uabs_T[0])
print 'Uabs_T/Ap: ' + str(Uabs_T[0]/Ap)

Qabs_Suzuki = 4.3712007458420821E-003
print 'according to suzuki, Qabs: ' + str(Qabs_Suzuki)
print 'so Cabs = Qabs*Ap = ' + str(Qabs_Suzuki*Ap)


print 'Uabs_local*4/3*pi*r^3 = ' + str(0.72473E+02*4./3.*np.pi*radshell**3.)

#Qabs_shell = tplquad(diff_Uabs, r2, r3, lambda r:   t1, lambda r:   t2,
#                                      lambda r,t: p1, lambda r,t: p2)[0]
#print 'Qabs_shell: ' + str(Qabs_shell)
#print 'Qabs (0.65...): ' + str(Qabs_core + Qabs_shell)
#Qabs = tplquad(diff_Uabs, r1, r3, lambda r:   t1, lambda r:   t2,
#                                        lambda r,t: p1, lambda r,t: p2)[0]

mlab.surf(xx,yy,interpslice,warp_scale='auto')
mlab.show()

#print Qabs