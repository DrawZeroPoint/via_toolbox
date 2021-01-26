#!/usr/bin/python
# -*- coding: UTF-8 -*-

#检查文件夹下的图片是不是都是三通道的

import os
import cv2

image_dir = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/val_pointer_new/"
image_list = os.listdir(image_dir)

for image_item in image_list:
    print(image_item)
    img = cv2.imread(image_dir + image_item)
    if img.shape[2] is not 3:
        print(image_item + '............................................................... is not 3 channels')
    print(img.shape[2])
