#!/usr/bin/env python3

import cv2

import matplotlib.pyplot as plt
import numpy as np

from asyncore import read
from copy import deepcopy
import readline
import  math
import itertools
import sys

if len(sys.argv) <= 1:
    print("no input")
    exit(1)

## Define 8 ANSI color
ansi_8_colors = np.array([
    [   0,   0,   0],
    [ 255,   0,   0],
    [   0, 255,   0],
    [   0,   0, 255],
    [ 255, 255,   0],
    [   0, 255, 255],
    [ 255,   0, 255],
    [ 255, 255, 255],
])
ansi_8_colors = cv2.cvtColor(ansi_8_colors.astype(np.uint8).reshape((2,4,3)), cv2.COLOR_BGR2LAB).reshape((8,3)).astype(np.float32)

## Load image
img = cv2.imread(sys.argv[1],1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)

## Compute distances
pd = ansi_8_colors.reshape((8, 1, 3)) - img.reshape((1, -1, 3))
pd = np.linalg.norm(pd, axis=2)

## Compute transformed colors
closes_idx = np.argmin(pd, axis=1)
new_colors = img.reshape((-1, 3))[closes_idx, :]
q = (1+math.sqrt(5))/2
q = 1/q
center_color = np.mean(new_colors, axis=0)
new_colors = q*new_colors + q*(1-q)*ansi_8_colors + (1-q)**2*center_color

# Darker colors
dir_col = new_colors[0,:] - new_colors[-1,:]
new_colors_sub = new_colors + 0.16*dir_col
new_colors_sub[0,:] -= 2*0.16*dir_col

new_colors_sub[0,:], new_colors[0,:] = 1*new_colors[0,:], 1*new_colors_sub[0,:]

## Assemble color matrix
colors = np.zeros((3,8,3))
colors[0,:,:] = ansi_8_colors
colors[1,:,:] = new_colors
colors[2,:,:] = new_colors_sub

img_rgb = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_LAB2RGB)
colors_rgb = cv2.cvtColor(colors.astype(np.uint8), cv2.COLOR_LAB2RGB)

## Plotting
Hplt = 2
Wplt = 2

ax = plt.subplot(Hplt, Wplt, 1)
ax.imshow(img_rgb)

ax = plt.subplot(Hplt, Wplt, 2)
ax.imshow(colors_rgb)

ax = plt.subplot(Hplt, Wplt, 3)
ax.axis('equal')
ax.set_facecolor("gray")
sample_idx = np.random.permutation(img.size//3)[:100000]
ax.scatter(img.reshape((-1,3))[sample_idx,1], img.reshape((-1,3))[sample_idx,2], alpha=0.1, c='white', sizes=0.1*img.reshape((-1,3))[sample_idx,0])
c0 = np.ones((8, 4))
c1 = np.ones((8, 4))
c0[:,:3] = colors_rgb[0,:,:]/255
c1[:,:3] = colors_rgb[1,:,:]/255
ax.scatter(colors[0,:,1], colors[0,:,2], c=c0, marker='x', sizes=colors[0,:,0])
ax.scatter(colors[1,:,1], colors[1,:,2], c=c1, sizes=colors[1,:,0])

plt.show()
