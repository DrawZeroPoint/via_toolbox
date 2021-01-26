#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 随机分离训练集，验证集，测试机，比例7:2:1

import os
import random
import shutil


def each_file(filepath):
    path_dir = os.listdir(filepath)
    child_file_name = []
    full_child_file_list = []
    for all_dir in path_dir:
        child = os.path.join('%s%s' % (filepath, all_dir))
        full_child_file_list.append(child)
        child_file_name.append(all_dir)

    return full_child_file_list, child_file_name


if __name__ == '__main__':
    raw_img = "/home/gy/Database/Done/pointer_datase/images/train_pointer/"
    train_img = "/home/gy/Database/Done/pointer_datase/images/train/"
    val_img = "/home/gy/Database/Done/pointer_datase/images/val/"
    test_img = "/home/gy/Database/Done/pointer_datase/images/test/"

    image_list = os.listdir(raw_img)
    filePath, image_list = each_file(raw_img)
    print(filePath, image_list)
    random.shuffle(filePath)
    train_list = image_list[0:int(0.7 * len(image_list))]
    val_list = image_list[int(0.7 * len(image_list)):int(0.9 * len(image_list))]
    test_list = image_list[int(0.9 * len(image_list)):len(image_list)]
    for image_item in train_list:
        print(image_item)
        shutil.copy(raw_img + image_item,
                    train_img + image_item)
    for image_item in test_list:
        print(image_item)
        shutil.copy(raw_img + image_item,
                    test_img + image_item)
    for image_item in val_list:
        print(image_item)
        shutil.copy(raw_img + image_item,
                    val_img + image_item)
