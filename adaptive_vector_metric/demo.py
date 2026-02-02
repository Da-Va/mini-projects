from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

from math import *

N = 1000

lb, ub = -5, 5

Xax = np.linspace(lb, ub, N)
Yax = np.linspace(lb, ub, N)

XX, YY = np.meshgrid(Xax, Yax)


def get_next_ax(name=''):
    global ax_idx
    plt.subplot(ax_row, ax_col, ax_idx)
    plt.axis('equal')
    plt.title(name)
    ax_idx += 1
    
def plot_cont(ZZ):
    # plt.pcolor(XX, YY, ZZ)
    cnt = plt.contourf(XX, YY, ZZ, levels = 20)
    plt.colorbar(cnt)
    cnt = plt.contour(XX, YY, ZZ, levels = [1], cmap='plasma')
    plt.grid()
    
def q_2_inf(XX, YY):
    ZZ_2 = np.sqrt(XX**2 + YY**2)
    ZZ_inf = np.maximum(np.abs(XX), np.abs(YY))
    q = np.exp(-0.6*np.power(ZZ_inf-1, 2)) 
    ZZ = (((1-q)*ZZ_2) + (q*ZZ_inf))
    return ZZ

def q_sum(XX, YY):
    XX_ = deepcopy(XX)
    XX_[np.abs(XX_)<1.0] = 0.0
    YY_ = deepcopy(YY)
    YY_[np.abs(YY_)<1.0] = 0.0
    ZZ = np.sqrt(XX_**2 + YY_**2)
    # ZZ[ZZ == sqrt(1+0.25)] = 0
    ZZ -= 0
    return ZZ    

ax_row, ax_col = 2, 2
ax_idx = 1
def main():
    get_next_ax('q^2')
    ZZ = np.sqrt(XX**2 + YY**2)
    plot_cont(ZZ)

    get_next_ax('q_inf')
    ZZ = np.maximum(np.abs(XX), np.abs(YY))
    plot_cont(ZZ)

    # get_next_ax('q_3')
    # ZZ = np.power(np.abs(XX**3) + np.abs(YY**3), 1/3)
    # plot_cont(ZZ)

    get_next_ax('q_pi')
    # ZZ = q_2_inf(XX, YY)
    ZZ = q_sum(XX, YY)
    plot_cont(ZZ)

    plt.show()
    
if __name__=='__main__':
    main()