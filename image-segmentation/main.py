import sys
from copy import deepcopy

import cv2
import math

import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


def main(args):
    assert len(args) > 1, 'Missing image file argument'
    in_file_name = args[1]

    img = cv2.imread(in_file_name)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    img_hsv[:,:,0] = img_hsv[:,:,0] // 32 * 32
    tmp = deepcopy(img_hsv[:,:,2])
    img_hsv[:,:,2] = img_hsv[:,:,1]
    img_hsv[:,:,1] = 255

    img_transformed = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
    img_lab = cv2.cvtColor(img_transformed, cv2.COLOR_RGB2LAB)
    img_lab = cv2.blur(img_lab, (30,30))
    # img_lab[:,:,0] = np.power(img_lab[:,:,0]/255, 2) * 255

    pixel_vals = img_lab.reshape((-1,3))

    pixel_vals = np.float32(pixel_vals)

    # pixel_vals = np.zeros((pixel_vals.shape[0],4), np.uint8)
    # pixel_vals[:, :3] = img_lab.reshape((-1,3))
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         pixel_vals[i * img.shape[1] + j, 3] \
    #             = math.atan2(i - img.shape[0]/2, j - img.shape[1]/2) / math.pi * 0.1


    k = 2
    clustering = KMeans(k).fit(pixel_vals)

    label_cols = np.array([
        [0,0,0],
        # [0, 0, 50],
        # [120, 120, 120],
        [255, 0, 0]
    ], dtype=np.uint8)

    # segmented_data = label_cols[labels.flatten()]
    segmented_data = label_cols[clustering.labels_]

    segmented_image = segmented_data.reshape(img.shape)

    edges = cv2.Canny(img_transformed, 100, 200)

    # for i in range(3):
    #     kernel = np.ones((i*10,i*10), np.uint8)
    #     segmented_image = cv2.erode(segmented_image, kernel)
    #     segmented_image = cv2.dilate(segmented_image, kernel)
        # segmented_image = cv2.dilate(segmented_image, kernel)
        # segmented_image = cv2.erode(segmented_image, kernel)

    fig = plt.figure()
    ax = fig.add_subplot(2,2,1)
    ax.imshow(img)
    ax.imshow(segmented_image, alpha=0.5)
    ax = fig.add_subplot(2,2,2)
    ax.imshow(segmented_image)
    ax = fig.add_subplot(2,2,3)
    ax.imshow(img_transformed)
    ax = fig.add_subplot(2,2,4)
    ax.imshow(img)
    plt.show()

if __name__=='__main__':
    main(sys.argv)