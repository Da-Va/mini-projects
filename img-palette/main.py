#!/usr/bin/env python3

from asyncore import read
from copy import deepcopy
import readline
import sys

import numpy as np
import cv2

if len(sys.argv) <= 1:
    print("no input")
    exit(1)

img = cv2.imread(sys.argv[1],1)
cv2.imshow("original",img)

colors = np.array([
    [   0,  43,  54],
    [   7,  54,  66],
    [  88, 110, 117],
    [ 101, 123, 131],
    [ 131, 148, 150],
    [ 147, 161, 161],
    [ 238, 232, 213],
    [ 253, 246, 227],
    [ 181, 137,   0],
    [ 203,  75,  22],
    [ 220,  50,  47],
    [ 211,  54, 130],
    [ 108, 113, 196],
    [  38, 139, 210],
    [  42, 161, 152],
    [ 133, 153,   0],
])

q = 0.5

forward_conversion = cv2.COLOR_RGB2BGR
backward_conversion = cv2.COLOR_BGR2RGB

# preprocess
colors = cv2.cvtColor(colors.reshape((1,-1,3)).astype(np.float32), forward_conversion).reshape((-1,3))
Z = cv2.cvtColor(img.astype(np.float32), forward_conversion).reshape((-1,3))

# conversion
diff = Z.reshape((-1,3, 1)) - colors.T.reshape((1,3,-1))
w = np.linalg.norm(diff, axis=1)

# q = np.mean(np.min(w, axis=1)) / np.mean(np.max(w, axis=1))
q = np.min(np.mean(w, axis=1)) / np.max(np.mean(w, axis=1))

w = 1/w
w = w / np.sum(w, axis=1, keepdims=True)
w[np.isnan(w)] = 1.0
res = w @ colors

# consolidate result

print(q)
res = q*res + (1-q)*Z

res = res.reshape((img.shape))

res = cv2.cvtColor(res, backward_conversion)
res = np.round(res)
res = res.astype(np.uint8)


cv2.imshow("res",res)
cv2.waitKey()
cv2.destroyAllWindows()
