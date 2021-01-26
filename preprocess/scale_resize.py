#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import os

image_source_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/done_source/"
image_save_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/scale_resize/x2"

image_list = os.listdir(image_source_dir)

for image_item in image_list:
    img = cv2.imread(image_source_dir + image_item)
    # rows, cols = source.shape[:2]
    height, width = img.shape[:2]
    res = cv2.resize(img, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)

    img_save_path = image_save_dir + '/' + image_item
    cv2.imwrite(img_save_path, res)
