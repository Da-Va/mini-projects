#!/usr/bin/env python3

import sys
from xml.etree.ElementPath import xpath_tokenizer
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm

HEIGHT = 5
X_PADDING = 6
PAD_SIZE = 4
SCALE = 0.08

SPARSITY = 0.5

if __name__=='__main__':
    assert(len(sys.argv) > 5)
    height = int(sys.argv[1])
    width = int(sys.argv[2])
    spread = float(sys.argv[3])
    sparsity = float(sys.argv[4])
    outfname = sys.argv[5]
    
    heights = 2 * spread * np.random.random((height + 2*X_PADDING, width)) - 1 * spread
    mask = np.random.random((height + 2*X_PADDING, width))
    heights += HEIGHT
    heights[mask < SPARSITY] = 0
    
    heights[:X_PADDING,:] = HEIGHT
    heights[-X_PADDING:,:] = HEIGHT
    
    hf = np.kron(heights, np.ones((PAD_SIZE, PAD_SIZE)))
    hf *= SCALE
    
    start_y = width * SCALE / 2
    start_x = SCALE * X_PADDING/2
    
    goal_y = start_y
    goal_x = SCALE * (height + 1.5 * X_PADDING)
    
    with open(outfname, 'w') as outfile:
        np.savetxt(outfile, hf, delimiter=' , ')

    plt.show()