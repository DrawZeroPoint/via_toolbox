#!/usr/bin/env python
# encoding: utf-8

#通过修改gamma来生产曝光图片

import os
import cv2
import numpy as np


def gamma_trans(img, gamma):  # gamma函数处理
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
    return cv2.LUT(img, gamma_table)  # 图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。

source_img_dir = '/home/kilox/Database/Test/0_meter_recognition/0_test/20191030/20191030task'
blurred_img_dir = '/home/kilox/Database/Test/0_meter_recognition/0_test/20191030/20191030task_cropped'

image_list = os.listdir(source_img_dir)
for item in image_list:
    img = cv2.imread(source_img_dir + '/' + item)
    value_of_gamma = 10 * 0.01
    image_gamma_correct = gamma_trans(img, value_of_gamma)
    img_save_path = blurred_img_dir + '/' + item
    cv2.imwrite(img_save_path, image_gamma_correct)


