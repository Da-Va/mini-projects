#!/usr/bin/env python3

import cv2

import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy
import sys

ANSI_8_COLORS = np.array([
    [   0,   0,   0],
    [ 255,   0,   0],
    [   0, 255,   0],
    [   0,   0, 255],
    [ 255, 255,   0],
    [   0, 255, 255],
    [ 255,   0, 255],
    [ 255, 255, 255],
])
ANSI_8_COLORS_lab = cv2.cvtColor(
    ANSI_8_COLORS.astype(np.uint8).reshape((2,4,3)),
    cv2.COLOR_RGB2LAB).reshape((8,3)).astype(np.float32)

# Rigidly (+scale) aligns two point clouds with know point-to-point correspondences
# with least-squares error.
# Returns (scale factor c, rotation matrix R, translation vector t) such that
#   Q = P*cR + t
# if they align perfectly, or such that
#   SUM over point i ( | P_i*cR + t - Q_i |^2 )
# is minimised if they don't align perfectly.
def umeyama(P, Q):
    assert P.shape == Q.shape
    n, dim = P.shape

    centeredP = P - P.mean(axis=0)
    centeredQ = Q - Q.mean(axis=0)

    C = np.dot(np.transpose(centeredP), centeredQ) / n

    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    R = np.dot(V, W)

    # varP = np.var(a1, axis=0).sum()
    c = 1#/varP * np.sum(S) # scale factor

    t = Q.mean(axis=0) - P.mean(axis=0).dot(c*R)

    return c, R, t

def load_img_rgb(in_fn):
    img = cv2.imread(in_fn, 1)
    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
    return img

def load_palette(in_fn):
    cols = []
    with open(in_fn) as in_f:
        for line in in_f.readlines():
            cols.append(tuple(
                int(line.strip('#')[i:i+2], 16)
                for i in (0,2,4)
                ))
    return np.array(cols).reshape((1,-1,3))

def img_warp(img, palette):
    
    pd = palette.reshape((-1, 1, 3)) - img.reshape((1, -1, 3))
    pd = np.linalg.norm(pd, axis=2)
    closes_idx = np.argmin(pd, axis=1)

    samples = img.reshape((-1,3))[closes_idx,:]
    
    _, R, t = umeyama(samples, palette.reshape(-1,3))

    img_warped = img.reshape((-1,3)).dot(R) + t
    img_warped = img_warped.reshape(img.shape)
    
    return img_warped


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Missing input image.'
    img_fn = sys.argv[1]
    
    assert len(sys.argv) > 2, 'Missing color palette file.'
    palette_fn = sys.argv[2]

    img = load_img_rgb(img_fn)
    img_original = deepcopy(img)
    palette = load_palette(palette_fn)

    img_lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2LAB)
    palette_lab = cv2.cvtColor(palette.astype(np.uint8), cv2.COLOR_RGB2LAB)
    
    for i in range(0):
        print(f'Iteration: {i}')
        img_lab = img_warp(img_lab, palette_lab)
    img = cv2.cvtColor(img_lab.astype(np.uint8), cv2.COLOR_LAB2RGB)

    ax = plt.subplot(2, 2, 1)
    ax.imshow(img_original)
    ax = plt.subplot(2, 2, 3)
    ax.imshow(img)

    sample_idx = np.random.permutation(img.size//3)[:5000]
    ax = plt.subplot(1, 2, 2, projection='3d')
    ax.set_facecolor((0.3, 0.3, 0.3))
    ax.scatter(
        img_lab.reshape((-1, 3))[sample_idx, 1],
        img_lab.reshape((-1, 3))[sample_idx, 2],
        img_lab.reshape((-1, 3))[sample_idx, 0],
        alpha=0.1,
        c = img.reshape((-1,3))[sample_idx, :]/255
    )
    ax.scatter(
        ANSI_8_COLORS_lab.reshape((-1, 3))[:,1],
        ANSI_8_COLORS_lab.reshape((-1, 3))[:,2],
        ANSI_8_COLORS_lab.reshape((-1, 3))[:,0],
        alpha=1.0, marker='^',
        c = ANSI_8_COLORS.reshape((-1, 3))/255
    )
    ax.scatter(
        palette_lab.reshape((-1, 3))[:,1],
        palette_lab.reshape((-1, 3))[:,2],
        palette_lab.reshape((-1, 3))[:,0],
        alpha=1.0, marker='s',
        c = palette.reshape((-1, 3))/255
    )

    plt.show()
