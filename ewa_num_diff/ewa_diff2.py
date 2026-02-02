import numpy as np
import matplotlib.pyplot as plt

def ewa(Y, q):
    EWA_Y = np.zeros(Y.shape)
    a = -np.log(1-q)
    for i in range(Y.size):
        EWA_Y[i] = q * Y[i] + (1-q) * EWA_Y[i-1] if i > 0 else 0.0
    return EWA_Y

def diff(Y, s):
    DIFF = np.zeros(Y.shape)
    for i in range(Y.size):
        DIFF[i] = Y[i] - Y[i-1] if i > 0 else 0.0
        DIFF[i] /= s
    return DIFF

if __name__=='__main__':
    
    UB = 30
    N = 500
    s = 10

    X = np.linspace(0, UB, N)
    zero = np.zeros(X.shape)
    Y = 5*5*np.sin(0.2*X) + 2*np.sin(0.05*X) + s*0.1*np.sin(20*X)
    Y_d = 5*0.2*5*np.cos(0.2*X) + 0.05*2*np.cos(0.05*X) + 0*s*20*0.1*np.cos(20*X)
    
    q_1 = 0.4
    EWA_Y_1 = ewa(Y, q_1)

    q_2 = 0.5
    # q_2 = 1.0
    EWA_Y_2 = ewa(Y, q_2)
    
    Y_d_est = 30*(EWA_Y_2 - EWA_Y_1)

    plt.plot(X, zero, c='black')
    plt.plot(X, Y, c='blue')
    plt.plot(X, EWA_Y_1, c='green')
    # plt.plot(X, EWA_Y_2, c='cyan')

    plt.plot(X, Y_d, c='red')
    plt.plot(X, ewa(diff(Y, UB/N), 0.25), c='purple')
    plt.plot(X, Y_d_est, c='orange')
    plt.axis('equal')
    plt.show()