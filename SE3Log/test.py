#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from math import *

if __name__=='__main__':
    
    N = 101
    q = 10

    X = np.linspace(-pi/q, pi/q, N)
    print(X)
    
    Y = 1/X - 0.5/np.tan(X/2) 
    Z = X/10
    
    plt.plot(X, Y)
    plt.plot(X, Z)

    plt.axis('equal')
    plt.show()
    