#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import fnmatch
import os,sys
import json

ANNOTATION_DIR = "/home/kilox/via_project_10Jun2019_9h54m.json"
global false, null, true
false = null = true = ''

if __name__ == "__main__":
    f = open("/home/kilox/test.txt", 'rb')
    all_lines = f.readlines()
    for line in all_lines:
        name = re.findall(r'(.*).jpg', line)
        after_name = re.findall(r"\=\> (\d*)", line)
        file_str = open(ANNOTATION_DIR)
        setting = json.load(file_str)
        get_obj = json.dumps(setting)
        get_obj1 = get_obj
        info = name[0]+'.jpg'
        new_info = "0000000000"+after_name[0]+'.jpg'
        print(info, new_info)
        get_obj1 = eval(get_obj.replace(info, new_info))
        with open('{}'.format(ANNOTATION_DIR), 'w') as output_json_file:
            json.dump(get_obj1, output_json_file)
    f.close()
