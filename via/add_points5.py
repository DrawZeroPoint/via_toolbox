#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------------
# Copyright (c) Kilox Corporation. All rights reserved.
# Written by Gao Yi (yigaofire@gmail.com)
# This script aims to add visible attributes in previous annotation files
# ------------------------------------------------------------------------------

import json
import re
from pylab import *
from collections import OrderedDict
import warnings
import fnmatch
import os

warnings.filterwarnings("ignore")

# 路径图片,via生成json注释文档路径,生成的注释文档路径
# IMAGE_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/val_pointer_new"
# ANNOTATION_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/via_project_8Nov2019_16h20m (2).json"
# OUTPUT_ANNOTATION_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/val_pro.json"

IMAGE_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/12-25/images/train_pointer"
ANNOTATION_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/12-25/via_project_3.json"
OUTPUT_ANNOTATION_DIR = "/home/kilox/Database/Done/0_meter_recognition/pointer_process/12-25/via_project_5.json"

def filter_for_jpeg(root, files):
    """过滤图片文件

    :param root:
    :param files:
    :return:
    """
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    return files


def main():
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_jpeg(root, files)
        _via_img_metadata = {}
        for image_filename in image_files:
            index = image_filename.rfind('.')
            print(image_filename)
            afdex = image_filename.rfind('/')
            file_str = open(ANNOTATION_DIR)
            setting = json.load(file_str, object_pairs_hook=OrderedDict)
            get_obj = json.dumps(setting)
            info = re.findall(image_filename[afdex + 1:index] + r'.jpg+\d+', get_obj)
            output = setting.copy()
            obj_str = json.dumps(setting["_via_img_metadata"]["".join(info)])
            try:
                px_1 = int(re.findall(r"\"cx\"\: (.+?)\,", obj_str)[0])
                py_1 = int(re.findall(r"\"cy\"\: (.+?)\,", obj_str)[0])
                px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                py = re.findall(r"\"cy\"\: (.+?)\}", obj_str)
            except ValueError:
                try:
                    px_1 = int(re.findall(r"\"cx\"\: (.+?)\}", obj_str)[0])
                    py_1 = int(re.findall(r"\"cy\"\: (.+?)\,", obj_str)[0])
                    px = re.findall(r"\"cx\"\: (.+?)\}", obj_str)
                    py = re.findall(r"\"cy\"\: (.+?)\,", obj_str)
                except ValueError:
                    px_1 = int(re.findall(r"\"cx\"\: (.+?)\,", obj_str)[0])
                    py_1 = int(re.findall(r"\"cy\"\: (.+?)\}", obj_str)[0])
                    px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                    py = re.findall(r"\"cy\"\: (.+?)\}", obj_str)
            # print(px)
            # print(py)
            a = int(len(px) / 3)
            # print(a)
            regions = setting["_via_img_metadata"]["".join(info)]["regions"]
            for j in arange(a):
                item = {"shape_attributes": {}, "region_attributes": {"visible": "2"}}
                item["shape_attributes"]["name"] = "point"
                item["shape_attributes"]["cx"] = int((int(px[3 * j]) + int(px[1 + 3 * j])) / 2)
                item["shape_attributes"]["cy"] = int((int(py[3 * j]) + int(py[1 + 3 * j])) / 2)

                item2 = {"shape_attributes": {}, "region_attributes": {"visible": "2"}}
                item2["shape_attributes"]["name"] = "point"
                item2["shape_attributes"]["cx"] = int((int(px[3 * j + 1]) + int(px[2 + 3 * j])) / 2)
                item2["shape_attributes"]["cy"] = int((int(py[3 * j + 1]) + int(py[2 + 3 * j])) / 2)
                regions.insert(5 * j + 1, item)
                regions.insert(5 * j + 3, item2)

                _via_img_metadata[str(info[0])] = setting["_via_img_metadata"]["".join(info)]
                # print(_via_img_metadata[str(info[0])])
                # print(setting["_via_img_metadata"]["".join(info)]["regions"])
        output["_via_img_metadata"] = _via_img_metadata
    with open('{}'.format(OUTPUT_ANNOTATION_DIR), 'w') as output_json_file:
        json.dump(output, output_json_file)


if __name__ == "__main__":
    main()
