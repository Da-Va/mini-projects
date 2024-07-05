import numpy as np
import matplotlib.pyplot as plt

import sys

N=1000

L1 = 1
L2 = 0.8

def ik(x, y):
    t1 = (-x*x-y*y - L1**2 + L2**2)/(2*np.sqrt(x*x+y*y)*L1)
    a1 = np.arctan2(y, x) + np.arccos(t1)

    t2 = (x*x + y*y - L1**2 - L2**2)/(2*L1*L2)
    a2 = np.pi - np.arccos(t2)
    
    return a1, a2

def main(argv):
    XX, YY = np.meshgrid(np.linspace(-2, 2, N), np.linspace(-2, 2, N))
    
    A1, A2 = ik(XX, YY)
    
    # A1[A1>0] = np.nan
    # A1[A1<-np.pi/2] = np.nan
    
    ax = plt.subplot(1,2,1) 
    c = ax.contourf(XX, YY, A1, levels=60)
    plt.colorbar(c, ax=ax)
    
    ax = plt.subplot(1,2,2) 
    c = ax.contourf(XX, YY, A2, levels=60)
    plt.colorbar(c, ax=ax)
    

    plt.show()

    

if __name__=='__main__':
    main(sys.argv)