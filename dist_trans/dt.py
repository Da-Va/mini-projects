import sys

from cmath import nan
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

ieee_col_cm = .03514598035146 * 245.71811 * .3937008

if __name__=='__main__':

    sdf = np.zeros((100,100))
    
    for i in range(100):
        for j in range(100):
            sdf[i,j] = 60 - i - 10
            d = sqrt((i-60)**2 + (j-50)**2)
            if(d <= 20):
                sdf[i,j] += 20 - d

            # if sdf[i,j] > 0:
            #     sdf[i,j] = nan
                
    mm = sdf.min() if abs(sdf.min()) > abs(sdf.max()) else sdf.max()
    sdf[0,99] = -mm
    sdf = -sdf
            
    fig = plt.figure(figsize=(ieee_col_cm, ieee_col_cm))

    plt.imshow(sdf, cmap='coolwarm')
    plt.xticks([])
    plt.yticks([])
    plt.plot([0,99], [60,60], color='black', label='terrain')
    plt.scatter([49.9],[60], color='blue', label='foothold')
    plt.contour(sdf, 50, alpha=0.5, cmap='viridis')
    plt.contour(sdf, [0], colors='red')
    plt.plot([],[],color='red', label='collision boundary')
    plt.legend()
    
    if len(sys.argv) > 1:
        plt.savefig(sys.argv[1], backend='pgf')
    else:
        plt.show()