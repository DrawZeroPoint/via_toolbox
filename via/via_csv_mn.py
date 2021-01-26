#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
from collections import namedtuple
import json
import numpy as np
from json import JSONEncoder
from collections import deque
import os


class Object(object):
    def __init__(self):
        self.id = 0
        self.bbox = []
        self.corners = []
        self.digit_num = 0
        self.scale_points = []
        self.scale_numbers = []
        self.precision = 2


file_dir = "/home/kilox/Database/Test/0_meter_recognition/multi_pointer_temp/via_csv"
save_dir = "/home/kilox/Database/Test/0_meter_recognition/multi_pointer_temp/via_json"
file_list = os.listdir(file_dir)

for file_name in file_list:
    file = os.path.join(file_dir, file_name)
    with open(file) as f:
        readers = csv.reader(f)
        headings = next(readers)
        Row = namedtuple('Row', headings)
        # output = {'part_info_list': []}
        output = []
        items = {}

        item = Object()
        for i, rows in enumerate(readers):
            row = Row(*rows)
            if eval(row.region_shape_attributes)['name'] == 'point':
                item.scale_points.append(eval(row.region_shape_attributes)['cx'])
                item.scale_points.append(eval(row.region_shape_attributes)['cy'])
                item.scale_numbers.append(eval(row.region_attributes)['name'])
            else:
                item.bbox.append(eval(row.region_shape_attributes)['x'])
                item.bbox.append(eval(row.region_shape_attributes)['y'])
                item.bbox.append(eval(row.region_shape_attributes)['x'] + eval(row.region_shape_attributes)['width'])
                item.bbox.append(eval(row.region_shape_attributes)['y'] + eval(row.region_shape_attributes)['height'])
                item.id = eval(row.region_attributes)['name']
                output.append(item)
                # output['part_info_list'].append(item)
                item = Object()

        output_dict = [ob.__dict__ for ob in output]

        write_item_dict = {"part_info_list": output_dict}
        # 视觉感知组
        with open('{}'.format(save_dir + '/' + file_name[:-4] + '.json'), 'w') as output_json_file:
            json.dump(write_item_dict, output_json_file)
        # 系统部
        # with open('{}'.format(save_dir + '/' + file_name[:-4] + '.json'), 'w') as output_json_file:
        #     json.dump(output_dict, output_json_file)
        print("success!")
