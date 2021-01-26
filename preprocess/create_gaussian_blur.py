#!/usr/bin/env python
# encoding: utf-8

# 生成高斯模糊图像

import os
import cv2
import numpy as np


def gaussian_blur(image, ksize=(9, 9), sigmaX=0, sigmaY=0):
    # 高斯模糊（对焦模糊）
    # image = cv2.GaussianBlur(image, ksize=(degree, degree), sigmaX=0, sigmaY=0)

    blurred = cv2.GaussianBlur(image, ksize, sigmaX, sigmaY)
    return blurred


source_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/blur/source/5cm'
blurred_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/blur/gaussion_blur/2/5cm'

image_list = os.listdir(source_img_dir)
for item in image_list:
    img = cv2.imread(source_img_dir + '/' + item)
    # # 高斯模糊
    img_gaussian_blur = gaussian_blur(img, ksize=(77, 77))
    img_save_path = blurred_img_dir + '/' + '77x77' + '/' + item
    cv2.imwrite(img_save_path, img_gaussian_blur)
