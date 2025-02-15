import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm

from math import sin, cos, sqrt, ceil
N=1000
M = 3

def multi_plot():
    plot_funs = []
    for k, v in globals().items():
        if(callable(v)):
            spn = k.split('_')
            if(spn[0] == 'plot'):
                plot_funs.append((v, spn[1], ' '.join(spn[2:])))   
                
    plot_funs.sort(key=lambda t : t[2])
    if len(plot_funs) == 0:
        return

    w = ceil(sqrt(len(plot_funs)))
    h = ceil(len(plot_funs)/w)
    
    fig = plt.figure()
    
    for i, (f,p,n) in enumerate(plot_funs, start=1):
        print(f'subplot {w}{h}{i} ({p}) "{n}"')
        if p == '3d':
            ax = fig.add_subplot(h, w, i, projection=p)
        else:
            ax = fig.add_subplot(h, w, i)
        ax.set_title(n)
        f(ax)

    plt.show()

def ik(x, y):
    ds = x*x + y*y
    c1 = (ds + L1**2 - L2**2)/(2*np.sqrt(ds)*L1)
    a1 = np.arctan2(y, x) + np.arccos(c1)

    c2 = (L1**2 + L2**2 - ds)/(2*L1*L2)
    a2 = np.pi - np.arccos(c2)
    
    return a1, a2

def main(argv):
    XX, YY = np.meshgrid(np.linspace(-0, M, N), np.linspace(-M, 0, N))
    
    A1, A2 = ik(XX, YY)
    
    Lx = np.abs(XX) + np.abs(XX - np.cos(A1))
    Ly = np.abs(YY) + np.abs(YY - np.sin(A1))
    
    # A2[A1>np.pi/2] = np.nan
    # A2[A1<-0] = np.nan
    # A1[A1>np.pi/2] = np.nan
    # A1[A1<-0] = np.nan

    Lx[np.isnan(A1)] = np.nan
    Ly[np.isnan(A1)] = np.nan
    
    # IE = np.ones(XX.shape) * np.sum(np.abs(Lx))
    
    # ax = plt.subplot(1,3,3) 
    # ax.axis('equal')
    # ax.scatter(0,0)
    # c = ax.contourf(XX, YY, IE, levels=60)
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
    
multi_plot()

# ax = plt.subplot(1,3,1) 
# ax.axis('equal')
# ax.scatter(0,0)
# c = ax.contourf(XX, YY, A1, levels=60)
# plt.colorbar(c, ax=ax)

# ax = plt.subplot(1,2,1) 
# ax.axis('equal')
# c = ax.contourf(XX, YY, np.abs(A1), levels=60)
# plt.colorbar(c, ax=ax)
# ax.scatter([0,L1,L1],[0,0,-L2], c='red')
# ax.plot([0,L1,L1],[0,0,-L2], c='red')

# ax = plt.subplot(1,2,2) 
# ax.axis('equal')
# c = ax.contourf(XX, YY, 
#     np.maximum(np.abs(A1),np.abs(A2-np.pi/2)),
#     # np.maximum(np.abs(A1+np.pi/2),np.abs(A2-np.pi/2))
#     # +np.maximum(np.abs(A1-np.pi/2),np.abs(A2-np.pi/2)),
#     levels=60)
# plt.colorbar(c, ax=ax)
# ax.scatter([0,L1,L1],[0,0,-L2], c='red')
# ax.plot([0,L1,L1],[0,0,-L2], c='red')

