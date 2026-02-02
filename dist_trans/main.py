import numpy as np
import scipy.ndimage as spndi
import matplotlib.pyplot as plt


if __name__=='__main__':
    np.random.seed(314)
    XX, YY = np.meshgrid(np.linspace(-1,1,100), np.linspace(-1,1,100))

    sdf = np.random.random((100,100))
    sdf = spndi.gaussian_filter(sdf, 20)
    med = np.median(sdf)
    sdf[sdf>med] = 1
    sdf[sdf<=med] = 0
    sdf_pos = spndi.distance_transform_bf(sdf)
    sdf_neg = spndi.distance_transform_bf(1-sdf)
    sdf = sdf_pos - sdf_neg
    sdf = (XX[0,1] - XX[0,0]) * sdf
    
    fh = np.array((-0.52,-0.15))
    normal = np.array((0,1))
    normal = normal/np.linalg.norm(normal)
    
    margin = 0.1
    r = 0.3
    gamma = 0.5/r**2
    p = 8
    kernel = pow(1 +  (gamma/p)*((XX-fh[0])**2 + (r/margin)*(YY-fh[1])**2), -p)
    sdf_alt = sdf + 2*(margin)*kernel - r
    
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    
    ax1.pcolor(XX, YY, sdf, cmap='coolwarm')
    ax1.contour(XX, YY, sdf, [0, margin])
    ax1.scatter(fh[0], fh[1])
    
    ax2.pcolor(XX, YY, sdf_alt, cmap='coolwarm')
    ax2.contour(XX, YY, sdf, [0])
    ax2.contour(XX, YY, sdf_alt, [margin], colors=['yellow'])
    ax2.contour(XX, YY, sdf-r, [margin], colors=['green'])
    circ = plt.Circle(fh,r, fill=False)
    ax2.add_patch(circ)
    ax2.scatter(fh[0], fh[1])
    ax2.arrow(fh[0], fh[1], normal[0], normal[1])

    ax1.axis('equal')
    ax2.axis('equal')
    plt.show()
