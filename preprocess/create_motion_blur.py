#!/usr/bin/env python
# encoding: utf-8

# 生产运动模糊效果图像

import os
import cv2
import numpy as np


def motion_blur(image, degree=100, angle=20):
    # 运动模糊
    image = np.array(image)

    # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))

    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred


source_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/wutong_test/source'
blurred_img_dir = '/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/wutong_test/blurred_degree=20'

image_list = os.listdir(source_img_dir)
for item in image_list:
    print(item)
    img = cv2.imread(source_img_dir + '/' + item)
    # 运动模糊
    img_motion_blur = motion_blur(img, degree=7, angle=20)

    # cv2.namedWindow('motion_blur image', 0)
    # cv2.resizeWindow('motion_blur image', 640, 480)
    # cv2.imshow('motion_blur image', img_motion_blur)
    # cv2.waitKey()

    img_save_path = blurred_img_dir + '/' + item
    cv2.imwrite(img_save_path, img_motion_blur)
