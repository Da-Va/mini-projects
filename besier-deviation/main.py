import numpy as np
import matplotlib.pyplot as plt

N = 10
SAMPLING = 100


def main():
    P1 = np.zeros((2, N))
    for i in range(N):
        P1[:,i] = i/(N-1)
        
    P1 += 0.5 * (2*np.random.random(P1.shape)-1)


    dP1 = hodograph(P1)
    ddP1 = hodograph(dP1)

        
    # P2 = P1 + 0.01 * (2*np.random.random(P1.shape) - 1)
    P2 = P1
    P2[:,-1] += 0.01*(2*np.random.random((2,)) - 1)


    dP2 = hodograph(P2)
    ddP2 = hodograph(dP2)

    pi1 = curve(P1)
    dpi1 = curve(dP1)
    ddpi1 = curve(ddP1)

    pi2 = curve(P2)
    dpi2 = curve(dP2)
    ddpi2 = curve(ddP2)

    ax = plt.subplot(1, 3, 1)
    ax.set_aspect('equal')
    ax.scatter(P1[0,:], P1[1,:])
    ax.plot(pi1[0,:], pi1[1,:])
    ax.scatter(P2[0,:], P2[1,:])
    ax.plot(pi2[0,:], pi2[1,:])

    ax = plt.subplot(1, 3, 2)
    ax.set_aspect('equal')
    ax.scatter(dP1[0,:], dP1[1,:])
    ax.plot(dpi1[0,:], dpi1[1,:])
    ax.scatter(dP2[0,:], dP2[1,:])
    ax.scatter([0],[0])
    ax.plot(dpi2[0,:], dpi2[1,:])

    ax = plt.subplot(1, 3, 3)
    ax.set_aspect('equal')
    # ax.scatter(ddP1[0,:], ddP1[1,:])
    # ax.plot(ddpi1[0,:], ddpi1[1,:])
    # ax.scatter(ddP2[0,:], ddP2[1,:])
    # ax.plot(ddpi2[0,:], ddpi2[1,:])
    ax.scatter([0],[0])
    ax.plot(ddpi2[0,:]-ddpi1[0,:], ddpi2[1,:]-ddpi1[1,:])
    
    
    plt.show()


def hodograph(P):
    n = P.shape[1] - 1
    return n*(P[:,:-1] - P[:, 1:])    


def besier(P, t):
    if P.shape[1] == 2:
        return t*P[:,-1] + (1-t)*P[:,0]
    else:
        return t*besier(P[:,1:], t) + (1-t)*besier(P[:,:-1], t)


def curve(P):
    pi = np.array([
        besier(P, t)
        for t in np.linspace(0, 1, SAMPLING)]).T
    return pi


if __name__=='__main__':
    main()