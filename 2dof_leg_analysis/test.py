import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm

from math import sin, cos, sqrt, ceil

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

N=2000
M = 2.5

L1 = 1
L2 = 1.0

Y_slice = 0
        

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

x, y = 0.2, 0

a1,a2 = ik(x,y)

lx = abs(x) + abs(x - cos(a1))
ly = abs(y) + abs(y - sin(a1))

LB = np.maximum(
    np.abs(XX - x) * 1/lx,
    np.abs(YY - y) * 1/ly
)

def no_plot_3d_3_joint_ik_distance(ax):
    ax.plot_surface(XX,YY,
        np.maximum(
            np.maximum(np.abs(A1-a1), np.abs(A2-a2)),
            0*np.maximum(np.abs(x-XX),np.abs(y-YY))
        ), cmap=cm.viridis)

# def plot_3d_1_joint_2(ax):
#     ax.plot_surface(XX,YY,(A2-np.pi/2), cmap=cm.viridis)
# def plot_3d_2_joint_1(ax):
    ax.plot_surface(XX,YY,(A1), cmap=cm.viridis)

def plot_2d_1_joint_2(ax):
    ax.contourf(XX,YY,(A2-np.pi/2), cmap=cm.viridis, levels=100)
def plot_2d_2_joint_1(ax):
    ax.contourf(XX,YY,(A1), cmap=cm.viridis, levels=100)
def plot_2d_2_joint_3(ax):
    ax.contourf(XX,YY,(A1+A2), cmap=cm.viridis, levels=100)

def no_plot_3d_2_atan(ax):
    ax.plot_surface(XX,YY,np.abs(np.arctan2(YY, XX)), cmap=cm.viridis)
    
def no_plot_2d_1_joint_ik_distance(ax):
    ax.axis('equal')
    ax.contourf(XX,YY,
        np.maximum(
            np.maximum(np.abs(A1-a1), np.abs(A2-a2)),
            0*np.maximum(np.abs(x-XX),np.abs(y-YY))
        ),levels=100, cmap=cm.viridis)

    
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

