import numpy as np
import matplotlib.pyplot as plt

from math import pi as kPi

kN = 1000
k_dt = 0.1

if __name__=="__main__":

    t = np.linspace(0., 2*kPi, kN)
    s = np.sin(t)
    s_floor = np.sin(np.floor(t/k_dt) * k_dt)
    s_ceil = np.sin(np.ceil(t/k_dt) * k_dt)

    plt.plot(t, s)
    plt.plot(t, s_floor)
    plt.plot(t, s_ceil)

    plt.show()

    print("hello")