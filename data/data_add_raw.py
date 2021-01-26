#!/usr/bin/env python
# encoding: utf-8
# ------------------------------------------------------------------------------
# This script aims to add raw data to Database
# ------------------------------------------------------------------------------
import shutil
import sys
import os
import stat
import logging
import time
import json
from collections import OrderedDict


# log 配置 >=Debug的信息输出到stdout >=info的信息输出到log文件
logger = logging.getLogger('add_raw_data')
logger.setLevel(level=logging.DEBUG)

# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# FileHandler
file_handler = logging.FileHandler('CHANGELOG.log')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class TargetDir:
    def __init__(self, path):
        batch_number = 0
        numbers = os.listdir(path)
        if numbers:
            batch_number = int(max(numbers))

        self.path = path
        self.batch_number = batch_number

        # 获取文件夹中已经存在的图片的最大索引
        self.data_dir = os.path.join(self.path, str(self.batch_number).zfill(7), 'data')
        self.info_dir = os.path.join(self.path, str(self.batch_number).zfill(7), 'info')
        self.next_index = 0
        if os.path.exists(self.data_dir):
            index_arr = [int(os.path.splitext(index)[0]) for index in os.listdir(self.data_dir)]
            if index_arr:
                self.next_index = max(index_arr) + 1

        # 根据需要判断是否需要切换批次文件夹
        self.update()
        self.mode = 0o666 | stat.S_IRUSR

    # 插入data和Info
    def insert_data(self, source_data, source_info):
        # 由于Insertdata的时候一定要Insert info 所以将info的插入放在insertdata里面
        for (src_data, src_info) in zip(source_data, source_info):
            dst = os.path.join(self.data_dir,
                               '{}{}'.format((str(self.batch_number).zfill(7) + str(self.next_index).zfill(3)), os.path.splitext(src_data)[1]))
            shutil.copyfile(src_data, dst)
            logger.info('write image {} ==> {}'.format(src_data, dst))

            dst = os.path.join(self.info_dir,
                               '{}{}'.format((str(self.batch_number).zfill(7) + str(self.next_index).zfill(3)), os.path.splitext(src_info)[1]))
            if not os.path.exists(src_info):
                os.mknod(dst, self.mode)
            else:
                shutil.copyfile(src_info, dst)
                file_str = open(src_info)
                setting = json.load(file_str, object_pairs_hook=OrderedDict)
                name = os.path.basename(dst)
                setting["images"][0]["id"] = str(os.path.splitext(name)[0])
                with open('{}'.format(dst), 'w') as output_json_file:
                    json.dump(setting, output_json_file)
            logger.info('write info {} ==> {}'.format(src_info, dst))
            self.next_index += 1
            self.update()
        if source_data:
            logger.info('write [type] data({})'.format(len(source_data)))
        if source_info:
            logger.info('write info({})'.format(len(source_info)))

    # 当最大索引 >= 1000 时更新批次号
    def update(self):
        if self.next_index >= 1000:
            self.batch_number += 1
            self.data_dir = os.path.join(self.path, str(self.batch_number).zfill(7), 'data')
            self.info_dir = os.path.join(self.path, str(self.batch_number).zfill(7), 'info')
            self.next_index = 0
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.info_dir):
            os.makedirs(self.info_dir)
