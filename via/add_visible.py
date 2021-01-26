#!/usr/bin/python
# -*- coding: UTF-8 -*-

#读取json标注文件，更改其属性名称

import json
import os
import cv2
import re

filename = '/home/kilox/Database/Done/0_meter_recognition/pointer_process/12-25/pointer_single/via_project_5.json'
write_filename = '/home/kilox/Database/Done/0_meter_recognition/pointer_process/12-25/pointer_single/via_project_5_1.json'

with open(filename) as f:
    master_dicts = json.load(f)

_via_settings_dicts = master_dicts['_via_settings']
_via_img_metadata_dicts = master_dicts['_via_img_metadata']
i = 0
for key, value in _via_img_metadata_dicts.items():
    regions_list = value["regions"]
    for dict_item in regions_list:
        i = i + 1
        # print(i)
        regions_attributes_dict = dict_item["region_attributes"]
        # print(regions_attributes_dict)
        # if "name" in regions_attributes_dict:
        #     del regions_attributes_dict["name"]

        regions_attributes_dict["visible"] = "2"
        print(regions_attributes_dict)

write_item_dict = {'_via_settings': _via_settings_dicts, '_via_img_metadata': _via_img_metadata_dicts,
                           "_via_attributes": {"region": {"visible": {"type": "text", "description": "",
                                                                      "default_value": ""}}, "file": {}}}
print('ok')
with open(write_filename, 'w') as f:
    json.dump(write_item_dict, f)

