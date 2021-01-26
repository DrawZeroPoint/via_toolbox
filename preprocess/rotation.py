#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import os

image_source_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/2-match/done_source/"
image_save_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/2-match/rotation/180"

image_list = os.listdir(image_source_dir)

for image_item in image_list:
    print(image_item)
    img = cv2.imread(image_source_dir + image_item)
    rows, cols = img.shape[:2]

    M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), 180, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))

    img_save_path = image_save_dir + '/' + image_item
    cv2.imwrite(img_save_path, dst)
