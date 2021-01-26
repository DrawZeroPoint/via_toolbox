#!/usr/bin/env python
# encoding: utf-8

# 生产高斯噪点的图像

import os
import cv2
import numpy as np


def gaussian_noise(image, degree=None):
    # 随机添加扰动噪点
    row, col, ch = image.shape
    mean = 0
    if not degree:
        var = np.random.uniform(0.004, 0.01)
    else:
        var = degree
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = image + gauss
    cv2.normalize(noisy, noisy, 0, 255, norm_type=cv2.NORM_MINMAX)
    noisy = np.array(noisy, dtype=np.uint8)
    return noisy


source_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/blur/source1'
blurred_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/blur/gaussian_noise'

image_list = os.listdir(source_img_dir)
for item in image_list:
    img = cv2.imread(source_img_dir + '/' + item)
    # 高斯噪音
    img_gaussian_noise = gaussian_noise(img, degree=3000)
    img_save_path = blurred_img_dir + '/' + '3000' + '/' + item
    cv2.imwrite(img_save_path, img_gaussian_noise)
