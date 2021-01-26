#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------------------------------------------------------------
# Copyright (c) Kilox Corporation. All rights reserved.
# Written by Gao Yi (yigaofire@gmail.com)
# This script aims to change annotation files from via forms to coco forms for digital recognition
# ----------------------------------------------------------------------------------------------------------------
import json
import re
import fnmatch
from PIL import Image
from pylab import *
import os
import warnings

warnings.filterwarnings("ignore")

ROOT_DIR = os.getcwd()

IMAGE_DIR = "/home/kilox/roi-process"
ANNOTATION_DIR = "/home/kilox/roi-process/via_region_data.json"

INFO = {
    "description": "Keypoints Location of Digital Dataset",
    "url": "https://yigaoyi.github.io/",
    "version": "0.1.0",
    "year": 2019,
    "contributor": "Kilox Arithmetic",
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
        'keypoints': ["p0", "p1_one", "p1_two", "p1_three", "p1_four", "p1_five", "p1_six",
                      "p2_one", "p2_two", "p2_three", "p2_four", "p2_five", "p2_six",
                      "p3_one", "p3_two", "p3_three", "p3_four", "p3_five", "p3_six"],
        'skeleton': [[2, 3], [2, 4], [3, 5], [4, 5], [4, 6], [5, 7], [6, 7],
                     [8, 9], [8, 10], [9, 11], [10, 11], [10, 12], [11, 13], [12, 13],
                     [14, 15], [14, 16], [15, 17], [16, 17], [16, 18], [17, 19], [18, 19],
                     [20, 21], [20, 22], [21, 23], [22, 23], [22, 24], [23, 25], [24, 25]]
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


def main():
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    count = 0
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_jpeg(root, files)
        # go through each image
        for image_filename in image_files:
            print(image_filename)
            image = Image.open(image_filename)
            index = image_filename.rfind('.')
            afdex = image_filename.rfind('/')
            image_id = int(image_filename[afdex + 1:index])
            image_id = "%d" % image_id
            image_id = int(image_id)
            image_info = create_image_info(
                image_id, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)

            file_str = open(ANNOTATION_DIR)
            setting = json.load(file_str)
            get_obj = json.dumps(setting)
            info = re.findall(image_filename[afdex + 1:index] + r'.jpg+\d+', get_obj)
            if not info:
                print("{} is not exit in annotations!".format(image_filename))
            else:
                count = count + 1

                obj_str = json.dumps(setting["".join(info)])

                a = 0
                b = 0
                c = int(image.size[0])
                d = int(image.size[1])
                bbox = [a, b, c, d]

                x = a + c
                y = c + d
                segmentation = [x, y, a, y, a, b, x, b, x, y]

                px = re.findall(r"\"cx\"\: (.+?)\,", obj_str)
                py = re.findall(r"\"cy\"\: (.+?)\,", obj_str)
                points = []
                for i in arange(len(px)):
                    points.append(int(px[i]))
                    points.append(int(py[i]))
                    points.append(2)
                for i in arange(len(px), 25):
                    points.append(0)
                    points.append(0)
                    points.append(0)

                annotation_info = {
                    "id": count,
                    "image_id": image_id,
                    "category_id": 1,
                    "iscrowd": 0,
                    "area": c * d,
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "num_keypoints": 25,
                    "keypoints": points
                }
                coco_output["annotations"].append(annotation_info)

    with open('{}'.format(ANNOTATION_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
