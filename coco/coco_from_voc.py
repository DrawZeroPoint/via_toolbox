#!/usr/bin/python
import sys
import os
import json
import re
import xml.etree.ElementTree as ET
import datetime

START_BOUNDING_BOX_ID = 1
PRE_DEFINE_CATEGORIES = {}

INFO = {
    "description": "Keypoints Location of Pointer Dataset",
    "url": "https://yigaoyi.github.io/",
    "version": "1.0",
    "year": 2019,
    "contributor": "Kilox PerXeption Group",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if 0 < length != len(vars):
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        tempfilename = re.findall(r"\d+.jpg", filename)
        filename = os.path.splitext(tempfilename[0])[0]
        return int(filename)
    except:
        tempfilename = re.findall(r"\d+.JPG", filename)
        filename = os.path.splitext(tempfilename[0])[0]
        return int(filename)


def convert(xml_list, xml_dir, json_file):
    list_fp = open(xml_list, 'r')
    json_dict = {"info": INFO, "liceses": LICENSES, "images": [],  "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    for line in list_fp:
        line = line.strip()
        print("Processing %s" % (line))
        xml_f = os.path.join(xml_dir, line)
        print(xml_f)
        tree = ET.parse(xml_f + '.xml')
        root = tree.getroot()
        path = get(root, 'path')
        filename = os.path.splitext(line)[0] + '.jpg'

        # The filename must be a number
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width,
                 'id': image_id}
        json_dict['images'].append(image)
        # Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert (xmax > xmin)
            assert (ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id':
                image_id, 'bbox': [xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    categorie_ids = []
    for categorie, cid in categories.items():
        # 汽车项目更改
        cat = {'supercategory': 'none', 'id': categorie, 'name': categorie}
        # cat = {'supercategory': 'none', 'id': int(categorie), 'name': categorie}
        categorie_ids.append(categorie)
        # categorie_ids.append(int(categorie))
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    list_fp.close()
    print("=>=>=>=>=>=>=>=>=>=>=>\n\ncategories: ", categorie_ids, "\n\n=>=>=>=>=>=>=>=>=>=>=>")


if __name__ == '__main__':
    """The xmllist.txt is the list of xml file names to convert which can be created from separate.py
    The "xml_dir" is the place where all xmls located.
    """
    xml_list = "/home/gy/Database/Done/grape/voc/ImageSets/Main/trainval.txt"
    json_file = "/home/gy/Database/Done/grape/coco/annotations/ann_train_bbox.json"
    xml_dir = "/home/gy/Database/Done/grape/voc/Annotations"
    convert(xml_list, xml_dir, json_file)
