import numpy as np
import matplotlib.pyplot as plt


if __name__=='__main__':
    
    X = np.linspace(0, 30, 1000)
    Y = 5*np.sin(0.2*X) + 2*np.sin(0.05*X) #+ 0.1*np.sin(20*X)
    Y_d = 0.2*5*np.cos(0.2*X) + 0.05*2*np.cos(0.05*X) + 20*0.1*np.cos(20*X)
    
    EWA_Y = np.zeros(Y.shape)
    EWA_Y_d = np.zeros(Y.shape)
    EWA_Y_d_est = np.zeros(Y.shape)
    
    q = 0.2
    a = -np.log(1-q)
    for i in range(Y.size):
        EWA_Y[i] = q * Y[i] + (1-q) * EWA_Y[i-1] if i > 0 else 0.0
        EWA_Y_d[i] = q * Y_d[i] + (1-q) * EWA_Y_d[i-1] if i > 0 else 0.0

        EWA_Y_d_est[i] = q*Y[i] + a*EWA_Y[i]
    

    plt.plot(X, Y, c='black')
    plt.plot(X, Y_d, c='red')
    plt.plot(X, EWA_Y, c='blue')
    plt.plot(X, EWA_Y_d_est, c='purple')
    plt.plot(X, EWA_Y_d, c='green')
    plt.axis('equal')
    plt.show()