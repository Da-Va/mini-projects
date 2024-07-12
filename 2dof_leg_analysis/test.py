import numpy as np
import matplotlib.pyplot as plt

import sys

N=1000
M = 2.5

L1 = 1
L2 = 1.0

Y_slice = 0

def ik(x, y):
    ds = x*x + y*y
    c1 = (ds + L1**2 - L2**2)/(2*np.sqrt(ds)*L1)
    a1 = np.arctan2(y, x) + np.arccos(c1)

    c2 = (L1**2 + L2**2 - ds)/(2*L1*L2)
    a2 = np.pi - np.arccos(c2)
    
    return a1, a2

def multi_plot(plot_funs, rows=1):
    w = len(plot_funs)

def main(argv):
    XX, YY = np.meshgrid(np.linspace(-M, M, N), np.linspace(-M, M, N))
    
    A1, A2 = ik(XX, YY)
    
    Lx = np.abs(XX) + np.abs(XX - np.cos(A1))
    Ly = np.abs(YY) + np.abs(YY - np.sin(A1))
    
    
    # A2[A1>np.pi/2] = np.nan
    # A2[A1<-0] = np.nan
    # A1[A1>np.pi/2] = np.nan
    # A1[A1<-0] = np.nan

    Lx[np.isnan(A1)] = np.nan
    Ly[np.isnan(A1)] = np.nan
    
    # ax = plt.subplot(1,3,1) 
    # ax.axis('equal')
    # ax.scatter(0,0)
    # c = ax.contourf(XX, YY, A1, levels=60)
    # plt.colorbar(c, ax=ax)
    
    ax = plt.subplot(1,2,1) 
    ax.axis('equal')
    c = ax.contourf(XX, YY, Lx, levels=60)
    plt.colorbar(c, ax=ax)
    ax.scatter([0,L1,L1],[0,0,-L2], c='red')
    ax.plot([0,L1,L1],[0,0,-L2], c='red')

    ax = plt.subplot(1,2,2) 
    ax.axis('equal')
    c = ax.contourf(XX, YY, Ly, levels=60)
    plt.colorbar(c, ax=ax)
    ax.scatter([0,L1,L1],[0,0,-L2], c='red')
    ax.plot([0,L1,L1],[0,0,-L2], c='red')
    

    plt.show()

    

if __name__=='__main__':
    main(sys.argv)