#!/usr/bin/env python
# coding=utf-8
# -------------------------------------------------------------------------------------------------
# Written by Gao Yi (yigaofire@gmail.com) and Dong Zhipeng (zhipengdongneu@gmail.com)
# This script aims to change annotation files from via forms to coco forms for digital recognition
# -------------------------------------------------------------------------------------------------

import json
import re
import fnmatch
from PIL import Image
from pylab import *
import os
import warnings

warnings.filterwarnings("ignore")

NUM_KEYPOINTS = 14

ROOT_DIR = os.getcwd()

INFO = {
    "description": "Keypoints Location of Digit Dataset",
    "url": "http://172.16.2.5:30000/PerXeption/Toolbox",
    "version": "1.0.0",
    "year": 2021,
    "contributor": "PreXeption Group",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'pointer',
        'supercategory': 'pointer',
        'keypoints': ["t_l", "t_c", "t_r", "l_t", "r_t", "c_l", "c_c",
                      "c_r", "l_b", "r_b", "b_l", "b_c", "b_r", "points"],
        'skeleton': [[1, 2], [1, 4], [2, 3], [3, 5], [4, 6], [5, 8], [6, 7],
                     [6, 9], [7, 8], [8, 10], [9, 11], [10, 13], [11, 12], [12, 13]]
    }
]


def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, name) for name in files]
    files = [f for f in files if re.match(file_types, f)]
    return files


def create_image_info(image_id, file_name, image_size,
                      date_captured=datetime.datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):
    image_info = {
        "id": image_id,
        "file_name": file_name,
        "width": image_size[0],
        "height": image_size[1],
        "date_captured": date_captured,
        "license": license_id,
        "coco_url": coco_url,
        "flickr_url": flickr_url
    }

    return image_info


def create_annotation_info(annotation_id, image_id, category_info, binary_mask, keypoints, num_keypoints,
                           image_size=None, tolerance=2, bounding_box=None, ):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_info["id"],
        "iscrowd": 0,
        "area": 0,
        "bbox": bounding_box.tolist(),
        "segmentation": [],
        "num_keypoints": num_keypoints,
        "keypoints": keypoints
    }

    return annotation_info


def run(image_dir, annotation_file_path):
    (annotation_dir_path, annotation_file_name) = os.path.split(annotation_file_path)
    save_anno_file_path = os.path.join(annotation_dir_path, "save_json.json")
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    for root, _, files in os.walk(image_dir):
        image_files = filter_for_jpeg(root, files)

        # Retrieve annotation info
        anno_file = open(annotation_file_path)
        setting = json.load(anno_file)
        _via_img_metadata = setting['_via_img_metadata']
        get_obj = json.dumps(setting)

        # Go through each image in image_dir
        for image_name in image_files:
            # print(image_filename)
            image = Image.open(image_name)
            visible_obj_num = image_name.rfind('.')
            afdex = image_name.rfind('/')
            image_id = int(image_name[afdex + 1:visible_obj_num])
            image_id = "%d" % image_id
            image_id = int(image_id)
            image_info = create_image_info(
                image_id, os.path.basename(image_name), image.size)
            coco_output["images"].append(image_info)

            anno_id = re.findall(image_name[afdex + 1:visible_obj_num] + r'.jpg+\d+', get_obj)
            if not anno_id:
                print("{} is not exit in annotations!".format(image_name))
            else:
                obj_str = json.dumps(_via_img_metadata["".join(anno_id)])
                bbox_num = len(re.findall(r"\"rect\"", obj_str))
                if bbox_num == 0:
                    pass
                else:
                    if bbox_num == 1:
                        iscrowd = 0
                    else:
                        iscrowd = 1

                    for i in range(bbox_num):
                        # a = int("".join(re.findall(r"\"x\"\: (.+?)\,", obj_str)))
                        a = int(re.findall(r"\"x\"\: (.+?)\,", obj_str)[i])
                        b = int(re.findall(r"\"y\"\: (.+?)\,", obj_str)[i])
                        c = int(re.findall(r"\"height\"\: (.+?)\}", obj_str)[i])
                        d = int(re.findall(r"\"width\"\: (.+?)\,", obj_str)[i])
                        bbox = [a, b, a+c, b+d]
                        x = a + c
                        y = c + d
                        segmentation = [x, y, a, y, a, b, x, b, x, y]

                        px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                        py = re.findall(r"\"cy\"\: (.+?)\}", obj_str)

                        points = []
                        num_keypoints = len(px)

                        for j in range(num_keypoints):
                            points.append(int(px[j]))
                            points.append(int(py[j]))
                            # 2 is for 'visible', we assume all labeled points are visible
                            points.append(2)

                        _id = int((image_id * 10) + i + 1)
                        annotation_info = {
                            "id": _id,
                            "image_id": image_id,
                            "category_id": 1,
                            "iscrowd": 0,
                            "area": c * d,
                            "bbox": bbox,
                            "segmentation": segmentation,
                            "num_keypoints": NUM_KEYPOINTS,
                            "keypoints": points
                        }
                        coco_output["annotations"].append(annotation_info)
        anno_file.close()

        with open('{}'.format(save_anno_file_path), 'w') as output_json_file:
            json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    from os.path import expanduser

    home = expanduser("~")
    IMAGE_DIR = '/home/dzp/Database/Done/pointer_10k/images/train_pointer'
    ANNOTATION_FILE = '//test/train_pro_via2.json'
    run(IMAGE_DIR, ANNOTATION_FILE)
