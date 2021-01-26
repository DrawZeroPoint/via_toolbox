#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import os

image_source_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/done_source/"
image_save_dir = "/home/kilox/Database/Test/0_meter_recognition/test_Identify_performance_range/Translation/Translation_100x50"

image_list = os.listdir(image_source_dir)

for image_item in image_list:
    img = cv2.imread(image_source_dir + image_item)
    rows, cols = img.shape[:2]
    M = np.float32([[1, 0, 100], [0, 1, 50]])
    dst = cv2.warpAffine(img, M, (cols, rows))
    img_save_path = image_save_dir + '/' + image_item
    cv2.imwrite(img_save_path, dst)


# cv2.imshow('source', source)
# cv2.imshow('dst', dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
