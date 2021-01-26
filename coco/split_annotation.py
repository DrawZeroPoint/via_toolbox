#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 根据图像文件夹分割标注文件

import json
import os
import re

root_dir = '/home/gy/Database/Done/pointer_dataset/'

via_all_json = os.path.join(root_dir, 'via_pro/via2_all.json')

via_train_json = os.path.join(root_dir, 'via_pro/via2_tarin.json')
via_test_json = os.path.join(root_dir, 'via_pro/via2_test.json')
via_val_json = os.path.join(root_dir, 'via_pro/via2_val.json')

img_train_dir = os.path.join(root_dir, 'images/train')
img_test_dir = os.path.join(root_dir, 'images/test')
img_val_dir = os.path.join(root_dir, 'images/val')


img_train_list = os.listdir(img_train_dir)
img_test_list = os.listdir(img_test_dir)
img_val_list = os.listdir(img_val_dir)


with open(via_all_json) as f:
    master_dicts = json.load(f)
    get_obj = json.dumps(master_dicts)

_via_settings_dicts = master_dicts['_via_settings']
_via_img_metadata_dicts = master_dicts['_via_img_metadata']

print('write pointer_train_json')
_via_img_metadata_dicts_train = {}

for img_item in img_train_list:
    index = img_item.rfind('.')
    afdex = img_item.rfind('/')
    info = re.findall(img_item[afdex + 1:index] + r'.jpg+\d+', get_obj)

    _via_img_metadata_dicts_train[info[0]] = _via_img_metadata_dicts[info[0]]

write_item_dict_train = {'_via_settings': _via_settings_dicts, '_via_img_metadata': _via_img_metadata_dicts_train,
                         "_via_attributes": {"region": {}, "file": {}}}
with open(via_train_json, 'w') as f:
    json.dump(write_item_dict_train, f)

print('write pointer_test_json')
_via_img_metadata_dicts_test = {}

for img_item in img_test_list:
    index = img_item.rfind('.')
    afdex = img_item.rfind('/')
    info = re.findall(img_item[afdex + 1:index] + r'.jpg+\d+', get_obj)

    _via_img_metadata_dicts_test[info[0]] = _via_img_metadata_dicts[info[0]]

write_item_dict_test = {'_via_settings': _via_settings_dicts, '_via_img_metadata': _via_img_metadata_dicts_test,
                        "_via_attributes": {"region": {}, "file": {}}}
with open(via_test_json, 'w') as f:
    json.dump(write_item_dict_test, f)


print('write pointer_test_json')
_via_img_metadata_dicts_test = {}

for img_item in img_val_list:
    index = img_item.rfind('.')
    afdex = img_item.rfind('/')
    info = re.findall(img_item[afdex + 1:index] + r'.jpg+\d+', get_obj)

    _via_img_metadata_dicts_test[info[0]] = _via_img_metadata_dicts[info[0]]

write_item_dict_test = {'_via_settings': _via_settings_dicts, '_via_img_metadata': _via_img_metadata_dicts_test,
                        "_via_attributes": {"region": {}, "file": {}}}
with open(via_val_json, 'w') as f:
    json.dump(write_item_dict_test, f)
